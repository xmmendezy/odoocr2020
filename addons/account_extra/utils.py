# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
from logging import getLogger
from json import load, dumps
from requests import post

logger = getLogger(__name__)

data = {}
with open('/etc/data.json', 'r') as data_file:
    data = load(data_file)


def send_to_gti(invoice, TipoDoc: str = 1):
    url = f'{data["url_base"]}?pUsuario={data["username"]}&pClave={data["password"]}&pNumCuenta={data["num_account"]}'
    data_header = {
        'FechaFactura': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        'TipoDoc': TipoDoc,
        'SituacionEnvio': 1,  # Consultar, pendiente
        'CantDeci': 1,  # Consultar, pendiente
        'Sucursal': 1,  # En variables externas
        'CodigoActividad': 851201,  # Consultar, pendiente
        'Terminal': 1,  # En variables externas
        'Moneda': 1,  # Solucion Odoo
        'MedioPago': [
            2
        ],  # Consultar, pendiente
        'CondicionVenta': 1,  # Fijo
        'Receptor': {
            'Nombre': invoice.partner_id.name,
            'TipoIdent': 1,
            'Identificacion': invoice.partner_id.vat if invoice.partner_id.vat else '',
            'NombComercial': invoice.partner_id.parent_id.name,
            'AreaTelefono': (lambda x: x[1:x.find(')')])(invoice.partner_id.phone),
            'NumTelefono': (lambda x: x[x.find(')') + 1:].replace('-', ''))(invoice.partner_id.phone),
            'Destinatario': invoice.partner_id.name,
            'CodInterno': invoice.partner_id.vat if invoice.partner_id.vat else invoice.partner_id.name
        }
    }
    data_lineas = []
    discount_neto = Decimal('0.00')
    for invoice_line in invoice.invoice_line_ids:
        value_i = Decimal(invoice_line.quantity)*Decimal(invoice_line.price_unit)
        value_f = value_i*Decimal(1 - Decimal(invoice_line.discount/100))
        data_invoice_line = {
            'Cantidad': invoice_line.quantity,
            'UnidadMedida': 0,
            'Descripcion': invoice_line.product_id.name,
            'PrecioUnitario': invoice_line.price_unit,
            'Impuestos': []
        }
        if value_i - value_f > 0:
            discount_neto += value_i - value_f
            data_invoice_line['Descuentos'] = [
                {
                    'MontoDescuento': float(value_i - value_f),
                    'DetalleDescuento': 'Se aplica descuento.'
                }
            ]
        for tax in invoice_line.tax_ids:
            if tax.amount > 0:
                amount = Decimal(tax.amount/100)
            else:
                amount = Decimal('-1') * Decimal(tax.amount/100)
            data_invoice_line['Impuestos'].append({
                'CodigoImp': tax.CodigoImp,
                'CodigoTarifa': tax.CodigoTarifa,
                'MontoImp': float(value_f * amount)
            })
            # Analizar exoneracion
        data_lineas.append(data_invoice_line)
    data_total = {
        'TotalVenta': float(Decimal(invoice.amount_untaxed) - discount_neto),
        'TotalDescuento': float(discount_neto),
        'TotalVentaNeta': invoice.amount_untaxed,
        'TotalImpuesto': float(Decimal(invoice.amount_total) - Decimal(invoice.amount_untaxed)),
        'TotalComprobante': invoice.amount_total,
    }
    payload = {
        'NumCuenta': data["num_account"],
        'Documentos': [
            {
                'Encabezado': data_header,
                'Lineas': data_lineas,
                'Totales': data_total,
            },
        ]
    }
    print(data, url)
    r = post(url, json=dumps(payload), headers={'content-type': 'application/json'}, auth=(data['username'], data['password']))
    print(r.text)
    logger.info(f'Response Messages: {r.text}')

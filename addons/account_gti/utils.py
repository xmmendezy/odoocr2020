# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from logging import getLogger
from json import load, loads, dumps
from requests import post
from odoo.exceptions import ValidationError

logger = getLogger(__name__)


def send_to_gti(invoice, TipoDoc: int = 1, reason: str = ''):
    data = {}
    data_doc = {}
    with open('/etc/odoo/data.json', 'r') as data_file:
        data = load(data_file)
        data_doc = data['data_doc']
    try:
        EconomicActivity = int(invoice.EconomicActivity)
    except Exception:
        raise ValidationError('Sin actividad economica seleccionada')
    try:
        data_header = {
            'TipoDoc': TipoDoc,
            'SituacionEnvio': 1,  # Consultar, pendiente
            'CantDeci': 2,
            'Sucursal': data_doc['Sucursal'],
            'CodigoActividad': EconomicActivity,
            'Terminal': data_doc['Terminal'],
            'Moneda': invoice.currency_id.CodigoMoneda,
            'TipoCambio': invoice.currency_id.rate,
            'CondicionVenta': 1,
            'Receptor': {
                'Nombre': invoice.partner_id.name,
                'TipoIdent': 1,
                'Identificacion': invoice.partner_id.vat if invoice.partner_id.vat else '',
                'NombComercial': invoice.partner_id.parent_id.name,
                'AreaTelefono': (lambda x: int(x[1:x.find(')')]))(invoice.partner_id.phone),
                'NumTelefono': (lambda x: int(x[x.find(')') + 1:].replace('-', '')))(invoice.partner_id.phone),
                'Destinatario': invoice.partner_id.name,
                'CodInterno': invoice.partner_id.ref if invoice.partner_id.ref else invoice.partner_id.vat,
            }
        }
    except Exception:
        raise ValidationError('Formulario incompleto')
    if TipoDoc in [1, 3]:
        data_header['MedioPago'] = [1]
    else:
        data_header['MedioPago'] = []
    data_lineas = []
    discount_neto = Decimal('0.00')
    TotalServGravado = Decimal('0.00')
    TotalServExento = Decimal('0.00')
    TotalMercaGravada = Decimal('0.00')
    TotalMercaExenta = Decimal('0.00')
    TotalImpuesto = Decimal('0.00')
    for invoice_line in invoice.invoice_line_ids:
        value_i = Decimal(invoice_line.quantity)*Decimal(invoice_line.price_unit)
        value_f = value_i*Decimal(1 - Decimal(invoice_line.discount/100))
        data_invoice_line = {
            'Codigo': invoice_line.product_id.default_code,
            'Cantidad': invoice_line.quantity,
            'UnidadMedida': 1,  # Revisar
            'Descripcion': invoice_line.product_id.name,
            'PrecioUnitario': invoice_line.price_unit,
            'BaseImponible': float(value_f),
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
        is_exento = True
        MontoImpuesto = Decimal('0.00')
        for tax in invoice_line.tax_ids:
            if tax.amount > 0:
                amount = Decimal(tax.amount/100)
            else:
                amount = Decimal('-1') * Decimal(tax.amount/100)
            if is_exento:
                is_exento = amount == Decimal('0.00')
            mont_imp = value_f * amount
            MontoImpuesto += mont_imp
            data_invoice_line['Impuestos'].append({
                'CodigoImp': tax.CodigoImp,
                'CodigoTarifa': tax.CodigoTarifa,
                'PorcentajeImp': float(tax.amount),
                'MontoImp': float(mont_imp)
            })
            # Analizar exoneracion
        TotalImpuesto += MontoImpuesto
        if invoice_line.product_id.type == 'consu':
            if is_exento:
                TotalMercaExenta += value_i
            else:
                TotalMercaGravada += value_i
        else:
            if is_exento:
                TotalServExento += value_i
            else:
                TotalServGravado += value_i
        data_lineas.append(data_invoice_line)
    data_total = {
        'TotalServGravado': float(TotalServGravado),
        'TotalServExento': float(TotalServExento),
        'TotalServExonerado': 0.0,
        'TotalMercaGravada': float(TotalMercaGravada),
        'TotalMercaExenta': float(TotalMercaExenta),
        'TotalMercaExonerada': 0.0,
        'TotalGravado': float(TotalServGravado + TotalMercaGravada),
        'TotalExento': float(TotalServExento + TotalMercaExenta),
        'TotalExonerado': 0.0,
        'TotalIVADevuelto': 0.0,
        'TotalOtrosCargos': 0.0,
        'TotalVenta': float(Decimal(invoice.amount_untaxed) - discount_neto),
        'TotalDescuento': float(discount_neto),
        'TotalVentaNeta': invoice.amount_untaxed,
        'TotalImpuesto': float(TotalImpuesto),
        'TotalComprobante': invoice.amount_total,
    }
    payload = {
        'NumCuenta': data['num_account'],
        'Documentos': [
            {
                'Encabezado': data_header,
                'Lineas': data_lineas,
                'Totales': data_total,
            },
        ]
    }
    if TipoDoc == 3:
        payload['Documentos'][0]['Referencia'] = {
            'TipoDocRef': 1,
            'NumeroRef': invoice.NumeroRef,
            'FechaRef': invoice.FechaRef,
            'AccionRef': 1,
            'RazonNota': reason
        }
    r = post(f'{data["url_base"]}?pUsuario={data["username"]}&pClave={data["password"]}&pNumCuenta={data["num_account"]}', dumps(payload), headers={'content-type': 'application/json'}, auth=(data['username'], data['password']))
    response = loads(r.text)
    print(r.text)
    logger.info(f'Response Messages: {r.text}')
    if response['Respuestas'][0]['Codigo'] == 0:
        if TipoDoc == 1:
            invoice.NumeroRef = response['Respuestas'][0]['ClaveNumerica']
            invoice.FechaRef = response['Fecha']
    else:
        raise ValidationError(response['Respuestas'][0]['Detalle'])

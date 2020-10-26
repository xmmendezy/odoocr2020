# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
import requests
import logging
from odoo import models, fields, api
from json import dumps

logger = logging.getLogger(__name__)


class InvoiceGTI(models.Model):

    _inherit = 'account.move'

    def send_to_gti(self):
        num_account = 5002,
        auth = {
            'username': 'ivila@grupo-jgf.com',
            'password': 'CtaGTI*2017',
        } # En variables externas
        url = f'http://pruebas.gticr.com/AplicacionFEPruebas/ApiCargaFactura/api/Documentos/CargarDocumento?pUsuario={auth["username"]}&pClave={auth["password"]}&pNumCuenta={num_account}'
        data_header = {
            'FechaFactura': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            'TipoDoc': 1, #Variable
            'SituacionEnvio': 1, # Consultar, pendiente
            'CantDeci': 3, # Consultar, pendiente
            'Sucursal': 2, # En variables externas
            'CodigoActividad': 851201, # Consultar, pendiente
            'Terminal': 1, # En variables externas
            'Moneda': 1, # Solucion Odoo
            'MedioPago': [
                2
            ], # Consultar, pendiente
            'CondicionVenta': 1, # Fijo
            'Receptor': {
                'Nombre': self.partner_id.name,
                'TipoIdent': 1,
                'Identificacion': self.partner_id.vat if self.partner_id.vat else '',
                'NombComercial': self.partner_id.parent_id.name,
                'AreaTelefono': (lambda x: x[1:x.find(')')])(self.partner_id.phone),
                'NumTelefono': (lambda x: x[x.find(')') + 1:].replace('-', ''))(self.partner_id.phone),
                'Destinatario': self.partner_id.name,
                'CodInterno': self.partner_id.vat if self.partner_id.vat else self.partner_id.name
            }
        }
        data_lineas = []
        discount_neto = Decimal('0.00')
        for invoice in self.invoice_line_ids:
            value_i = Decimal(invoice.quantity)*Decimal(invoice.price_unit)
            value_f = value_i*Decimal(1 - Decimal(invoice.discount/100))
            data_invoice = {
                'Cantidad': invoice.quantity,
                'UnidadMedida': 0,
                'Descripcion': invoice.product_id.name,
                'PrecioUnitario': invoice.price_unit,
                'Impuestos': []
            }
            if value_i - value_f > 0:
                discount_neto += value_i - value_f
                data_invoice['Descuentos'] = [
                    {
                        'MontoDescuento': float(value_i - value_f),
                        'DetalleDescuento': 'Se aplica descuento.'
                    }
                ]
            for tax in invoice.tax_ids:
                if tax.amount > 0:
                    amount = Decimal(tax.amount/100)
                else:
                    amount = Decimal('-1') * Decimal(tax.amount/100)
                data_invoice['Impuestos'].append({
                    'CodigoImp': '',  # Completar
                    'CodigoTarifa': '',  # Completar
                    'MontoImp': float(value_f * amount)
                })
				# Analizar exoneracion
            data_lineas.append(data_invoice)
        data_total = {
            'TotalVenta': float(Decimal(self.amount_untaxed) - discount_neto),
            'TotalDescuento': float(discount_neto),
            'TotalVentaNeta': self.amount_untaxed,
            'TotalImpuesto': float(Decimal(self.amount_total) - Decimal(self.amount_untaxed)),
            'TotalComprobante': self.amount_total,
        }
        payload = {
            'NumCuenta': num_account,
            'Documentos': [
                {
                    'Encabezado': data_header,
                    'Lineas': data_lineas,
                    'Totales': data_total,
                },
            ]
        }
		print(payload)
        r = requests.post(url, json=dumps(payload), headers={'content-type': 'application/json'}, auth=(auth['username'], auth['password']))
        # print(r)
        # print(r.text)
        logger.info(f'Response Messages: {r.text}')

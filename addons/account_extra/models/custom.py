# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..utils import send_to_gti
from json import load


class InvoiceGTI(models.Model):

    _inherit = 'account.move'

    @api.model
    def _default_economic_activities_list(self):
       ls = self._get_economic_activities_list()
       if len(ls):
         return ls[0][0]
       else:
         return ''

    @api.model
    def _get_economic_activities_list(self):
        data = {}
        with open('/etc/odoo/data.json', 'r') as data_file:
            data = load(data_file)
        return data.get('EconomicActivity', [])

    NumeroRef = fields.Char()
    FechaRef = fields.Char()
    EconomicActivity = fields.Selection(selection=_get_economic_activities_list, string='EconomicActivity', default=_default_economic_activities_list)

    def action_post(self):
        send_to_gti(self, 1)
        super(InvoiceGTI, self).action_post()



class ReservalGTI(models.TransientModel):

    _inherit = 'account.move.reversal'

    def reverse_moves(self):
        send_to_gti(self.move_ids, 3, self.reason)
        super(ReservalGTI, self).reverse_moves()


class TaxGTI(models.Model):

    _inherit = 'account.tax'

    CodigoImp = fields.Integer(default=1)
    CodigoTarifa = fields.Integer(default=8)


class ResCurrencyGTI(models.Model):

    _inherit = 'res.currency'

    CodigoMoneda = fields.Integer(default=0)

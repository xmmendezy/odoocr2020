# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..utils import send_to_gti


class InvoiceGTI(models.Model):

    _inherit = 'account.move'

    NumeroRef = fields.Char()
    FechaRef = fields.Char()

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




# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..utils import send_to_gti


class InvoiceGTI(models.Model):

    _inherit = 'account.move'

    def action_post(self):
        super(InvoiceGTI, self).action_post()
        send_to_gti(self, 1)

class TaxGTI(models.Model):

    _inherit = 'account.tax'

    CodigoImp = fields.Integer(default=1)
    CodigoTarifa = fields.Integer(default=1)

class ResCurrencyGTI(models.Model):

    _inherit = 'res.currency'

    CodigoMoneda = fields.Integer(default=0)

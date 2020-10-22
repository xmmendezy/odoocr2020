# -*- coding: utf-8 -*-

from odoo import models

class AccountMove(models.Model):
    _inherit = "account.move"

    def post(self):
        print('************************** Hola ***************************')
        return super(AccountMove, self).post()

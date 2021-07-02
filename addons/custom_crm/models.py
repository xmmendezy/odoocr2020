# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):

    _inherit = 'account.move'

    def action_post(self):
        print('Hola Xavier, eres increible')
        super(AccountMove, self).action_post()
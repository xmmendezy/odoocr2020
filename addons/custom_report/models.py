# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    image_small = fields.Binary("Imagen", related="product_id.image_1920")

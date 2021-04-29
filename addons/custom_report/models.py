# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, tools
from zlib import compress
from codecs import decode

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    image_small = fields.Binary("Imagen", related="product_id.image_1920")

    @api.model
    def image_compress(self):
        return tools.image.ImageProcess(self.image_small).crop_resize(500 ,500).image_base64()

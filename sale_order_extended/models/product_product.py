from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    deposit_product_id = fields.Many2one(string="Deposit Product", help="Deposit product id",
                                         comodel_name="product.product")
    deposit_product_qty = fields.Integer(string="Deposit Product Qty", help="Deposit product qty")
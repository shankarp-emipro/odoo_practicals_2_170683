from odoo import fields, models


class ProductUom(models.Model):
    _name = "product.uom.ept4"
    _description = "To store product uom"

    name = fields.Char(string="Product UOM", help="Enter product uom")
    uom_category_id = fields.Many2one(string="UOM Category", help="UOM Category",
                                      comodel_name="product.uom.category.ept4", ondelete="cascade")

from odoo import fields, models


class ProductUomCategory(models.Model):
    _name = "product.uom.category.ept4"
    _description = "To store product uom category"

    name = fields.Char(string="Product UOM Category Name", help="Enter product uom category name",
                       required=True)
    uom_ids = fields.One2many(string="UOM Ids", help="UOM ids", comodel_name="product.uom.ept4",
                              inverse_name="uom_category_id")

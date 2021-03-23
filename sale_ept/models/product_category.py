from odoo import fields, models


class ProductCategory(models.Model):
    _name = "product.category.ept4"
    _description = "To store product category"

    name = fields.Char(string="Product Category Name", help="Enter product category name",
                       required=True)
    parent_id = fields.Many2one(string="Parent", help="Parent id",
                                comodel_name="product.category.ept4")

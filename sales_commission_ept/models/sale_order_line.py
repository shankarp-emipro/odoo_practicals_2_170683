from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tax_id = fields.Many2one(string="Tax", help="Tax", comodel_name="account.tax")

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    shipping_id = fields.Many2one(string="Shipping", help="Shipping id",
                                  comodel_name="product.product")
    partner_ept_id = fields.Many2one(string="Partner", help="Partner", comodel_name="res.partner")

    days = fields.Selection(selection=[
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday')
    ], string="Days", help="Days of the week")

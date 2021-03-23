from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax.ept"

    tax_use = fields.Selection(selection_add=[('Rent', 'Rent')])
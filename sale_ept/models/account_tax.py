from odoo import fields, models


class AccountTax(models.Model):
    _name = "account.tax.ept"
    _description = "To store account tax description"

    name = fields.Char(string="Tax Name", help="Descriptive name of the tax", required=True)
    tax_use = fields.Selection(selection=[
        ('None', 'None'),
        ('Sales', 'Sales'),
        ('Purchase', 'Purchase')
    ], string="Use of tax", help="Use of the tax")
    tax_value = fields.Float(string="Amount", help="Tax amount to apply")
    tax_amount_type = fields.Selection(selection=[
        ('Percentage', 'Percentage'),
        ('Fixed', 'Fixed')
    ], string="TaxAmount Type", help="Type of the applied text", default="Percentage")

from odoo import models, fields


class Invoices(models.TransientModel):
    _name = "invoices"

    partner_invoice_id = fields.Many2one(string="Partner Invoice", help="Partner invoice id",
                                         comodel_name="partner.invoices")
    invoice_id = fields.Many2one(string="Invoice", help="Invoices", comodel_name="account.move")
    is_confirm = fields.Boolean(string="Confirm", help="Tick to confirm the invoice")

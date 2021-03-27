from odoo import models, fields, api


class SalesCommissionLine(models.Model):
    _name = "sales.commission.line"
    _description = "To store sales commission line related data"

    commission_date = fields.Date(string="Date of commission", help="Date of the commission")
    partner_id = fields.Many2one(string="Partner", help="Partner id", comodel_name="res.partner")
    user_id = fields.Many2one(string="User", help="User id", comodel_name="res.users")
    source_document = fields.Char(string="Source of document", help="Source document")
    amount = fields.Float(string="Commission amount", help="Amount", digits=(6, 2))
    status = fields.Selection(selection=[
        ('Draft', 'Draft'),
        ('Paid', 'Paid')
    ], string="Commission Status", help="Status", default="Draft")
    is_paid_amount = fields.Boolean(string="Paid amount", help="Is Paid amount")
    sale_commission_id = fields.Many2one(string="Sale commission", help="Sale commission id",
                                         comodel_name="sales.commission.ept")

    @api.onchange('is_paid_amount')
    def _onchange_is_paid_amount(self):
        # Onchange of checkbox value state will be set accordingly
        # returns -
        if self.is_paid_amount:
            self.status = 'Paid'
        else:
            self.status = 'Draft'

    @api.onchange('status')
    def _onchange_status(self):
        # Onchange of status value checkbox will be checked accordingly
        # returns -
        if self.status == 'Paid':
            self.is_paid_amount = True
        else:
            self.is_paid_amount = False

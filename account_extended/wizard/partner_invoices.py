from odoo import models, fields, api


class PartnerInvoices(models.TransientModel):
    _name = "partner.invoices"

    partner_id = fields.Many2one(string="Partner", help="Partner id", comodel_name="res.partner",
                                 readonly=True)
    invoice_ids = fields.One2many(string="Invoices", help="Invoices",
                                  comodel_name="invoices", inverse_name="partner_invoice_id")

    def validate_invoices(self):
        # To validate the draft invoices
        # returns -
        self.invoice_ids.filtered(lambda invoice: invoice.invoice_id.action_post() if invoice.is_confirm is True else False)

    @api.model
    def default_get(self, fields):
        # To add invoice lines in the wizard
        # returns - dictionary
        result = super(PartnerInvoices, self).default_get(fields)

        draft_invoices = self.env['account.move'].search(
            [('partner_id', 'in', self.env.context['active_ids']), ('state', '=', 'draft')])

        invoice_lines = list(map(lambda draft_invoice: (0, 0, {'invoice_id': draft_invoice.id}),
                                 draft_invoices))

        result.update({'invoice_ids': invoice_lines})
        return result

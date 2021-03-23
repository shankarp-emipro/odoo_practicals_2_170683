import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    auto_validate_invoice = fields.Boolean(string="Auto Validate",
                                           help="Auto validate the invoices")

    def validate_invoices(self):
        # Opens the wizard popup and set the partner id in context
        # returns - action of the wizard
        action = self.env['ir.actions.act_window']._for_xml_id(
            "account_extended.action_partner_invoices_wizard")
        action['context'] = {'default_partner_id': self.id}
        return action

    def _auto_validate_invoice(self):
        # This is the corn job method to validate the draft invoices of the partners having
        # checked the boolean field named auto_validate_invoice
        # returns -
        _logger.info("Cron started to validate the draft invoices.")
        self.env['res.partner'].search([('auto_validate_invoice', '=', True)]).filtered(
            lambda partner:
            partner.invoice_ids.filtered(
                lambda invoice: invoice.state == 'draft').action_post())
        _logger.info("Draft invoices validated.")

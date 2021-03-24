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

    def register_payment(self):
        # To register the payment of the invoices which are in posted state
        # returns -
        fields = ['payment_date', 'amount', 'communication', 'group_payment', 'currency_id',
                  'journal_id', 'partner_bank_id', 'company_currency_id', 'line_ids',
                  'payment_type', 'partner_type', 'source_amount', 'source_amount_currency',
                  'source_currency_id', 'can_edit_wizard', 'can_group_payments', 'company_id',
                  'partner_id', 'payment_method_id', 'available_payment_method_ids',
                  'hide_payment_method', 'payment_difference', 'payment_difference_handling',
                  'writeoff_account_id', 'writeoff_label', 'show_partner_bank_account',
                  'require_partner_bank_account', 'country_code', 'payment_token_id',
                  'suitable_payment_token_partner_ids', 'payment_method_code']
        account_move_ids = self.env['account.move'].search(
            [('partner_id', '=', self.id), ('state', '=', 'posted')])
        for account_move in account_move_ids:
            res = self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=account_move_ids.ids).default_get(
                fields)
            temp = self.env['account.payment.register'].create(res)
            # test = self.env['account.payment.register'].search(
            #     [('partner_id', '=', self.id)]).mapped(lambda apr: apr.action_create_payments())
            temp2 = temp.action_create_payments()
            d = 1

        # temp = self.env['account.payment.register'].search(
        #     [('partner_id', '=', self.id)])

        f = 1
        # data = self.env['account.payment.register'].with_context(
        #     active_model='account.move', active_ids=account_move_ids,
        #     dont_redirect_to_payments=True).default_get(fields)
        # test = self.env['account.payment.register'].action_create_payments()
        x = 1

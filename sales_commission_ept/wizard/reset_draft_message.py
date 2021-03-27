from odoo import models, fields


class ResetDraftMessage(models.TransientModel):
    _name = "reset.draft.message"
    _description = "Wizard to enter the reason of resetting the state to draft"

    wizard_draft_reason = fields.Text(string="Reason of reset", help="Reason of reset",
                                      required=True)

    def reset_to_draft(self):
        """
        Resets all the commission's states to draft and then generates the log in chatter section
        about the draft reason. Also clears the paid date and sets the master commission's state
        to draft.
        :return: dictionary
        """
        sales_commission = self.env['sales.commission.ept'].browse(
            self._context['active_ids'])
        for commission in sales_commission.commission_lines_ids:
            commission.is_paid_amount = False
            commission.status = 'Draft'

        sales_commission.paid_date = None
        sales_commission.status = 'Draft'

        return self.env['sales.commission.ept'].browse(self._context['active_ids']).message_post(
            body=self.wizard_draft_reason)

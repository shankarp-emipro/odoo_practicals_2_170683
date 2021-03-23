from odoo import fields, models, api


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def action_sale_quotations_new(self):
        tag_id = self.env.ref('sale_order_extended.data_crm_tag_id1')
        action = super(CrmLead, self).action_new_quotation()
        action['context'].update({
            'default_crm_lead_id': self.id,
            'default_tag_ids': [(6, 0, tag_id.ids)]
        })
        return action

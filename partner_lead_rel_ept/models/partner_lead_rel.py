from odoo import fields, models, api


class PartnerLeadRel(models.Model):
    _name = "partner.lead.rel"
    _description = "To store the data of partner lead rel"

    name = fields.Char(string="Partner Lead", help="Sequence name of partner lead", readonly=True)
    from_date = fields.Date(string="From Date", help="From date")
    to_date = fields.Date(string="To Date", help="To date")
    partner_id = fields.Many2one(string="Partner", help="Partner id", comodel_name="res.partner")
    partner_contact_ids = fields.Many2many(string="Partner Contacts", help="Partner contacts ids",
                                           comodel_name="res.partner")
    salesperson_lead_count_ids = fields.One2many(string="Salesperson Lead Count", help="Salesperson lead count ids",
                                                 comodel_name="salesperson.lead.count",
                                                 inverse_name="partner_lead_id")
    lead_ids = fields.Many2many(string="Leads", help="Lead ids", comodel_name="crm.lead")
    total_revenue = fields.Float(string="Total Revenue", help="Total revenue", digits=(6, 2))
    message = fields.Text(string="Message", help="Enter some message")
    pipeline_count = fields.Integer(string="Pipeline Count", help="Count of pipeline of this salesperson",
                                    compute="_compute_pipeline_count")

    def _compute_pipeline_count(self):
        pipeline_count = self.env['crm.lead'].search_count(
            ['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_id.child_ids.ids)])
        self.pipeline_count = pipeline_count

    @api.model_create_multi
    def create(self, vals):
        # To generate unique sequence for partner lead
        # this is achieved by invoking the next_by_code() method of ir.sequence model
        # returns - record
        record = None
        for val in vals:
            val['name'] = self.env['ir.sequence'].next_by_code('partner.lead.rel')
            record = super(PartnerLeadRel, self).create(val)
        return record

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        # Onchange of the partner_id sets the total revenue
        # return -
        total_revenue = 0
        partner_and_contacts = self.env['crm.lead'].search(
            ['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_id.child_ids.ids)])

        for each_partner in partner_and_contacts:
            total_revenue += each_partner.expected_revenue

        self.total_revenue = total_revenue

    def get_pipeline_details(self):
        # fetches the data for creating the new record in salesperson_lead_count model
        # returns -
        if self.salesperson_lead_count_ids:
            self.salesperson_lead_count_ids.unlink()
            salesperson_lead_count_line = {
                'partner_lead_id': self.id,
                'partner_id': self.partner_id.id
            }
            self.env['salesperson.lead.count'].create(salesperson_lead_count_line)
        else:
            salesperson_lead_count_line = {
                'partner_lead_id': self.id,
                'partner_id': self.partner_id.id
            }
            self.env['salesperson.lead.count'].create(salesperson_lead_count_line)

    def view_leads(self):
        # sets the leads of the partner and its contacts
        # returns -
        partner_and_contacts = self.env['crm.lead'].search(
            ['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_id.child_ids.ids)])
        self.lead_ids = partner_and_contacts.ids

    def view_paid_orders(self):
        # To list out the paid orders
        # returns -
        return 0

from odoo import fields, models, api


class SalespersonLeadCount(models.Model):
    _name = "salesperson.lead.count"
    _description = "To store the data of salesperson lead count"

    partner_id = fields.Many2one(string="Salesperson", help="Name of the salesperson",
                                 comodel_name="res.partner")
    partner_lead_id = fields.Many2one(string="Partner Lead Id", help="Partner lead id", comodel_name="partner.lead.rel")
    pipeline_count = fields.Float(string="Pipeline Count", help="Count of pipeline of this salesperson", digits=(6, 2),
                                  compute="_compute_pipeline_count")
    total_revenue = fields.Float(string="Total Revenue", help="Total revenue of these leads", digits=(6, 2),
                                 compute="_compute_total_revenue")
    total_quotation = fields.Float(string="Total Quotation", help="Total no. of quotation created from these leads",
                                   digits=(6, 2),
                                   compute="_compute_total_quotation_and_sale_orders_and_sale_order_amount")
    total_sales_orders = fields.Float(string="Total Sales Orders",
                                      help="Total no. of sales orders created from these leads", digits=(6, 2),
                                      compute="_compute_total_quotation_and_sale_orders_and_sale_order_amount")
    total_sale_order_amount = fields.Float(string="Total Sale Order Amount",
                                           help="Sum of total order amounts of all these leads order", digits=(6, 2),
                                           compute="_compute_total_quotation_and_sale_orders_and_sale_order_amount")
    percentage_of_conversion = fields.Float(string="Percentage of Conversion",
                                            help="Percentage of conversion",
                                            digits=(6, 2), compute="_compute_percentage_of_conversion")

    def _compute_pipeline_count(self):
        pipeline_count = self.env['crm.lead'].search_count(
            ['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_id.child_ids.ids)])
        self.pipeline_count = pipeline_count

    def _compute_total_revenue(self):
        total_revenue = 0
        partner_and_contacts = self.env['crm.lead'].search(
            ['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_id.child_ids.ids)])

        for each_partner in partner_and_contacts:
            if each_partner.won_status == 'won':
                total_revenue += each_partner.expected_revenue

        self.total_revenue = total_revenue

    def _compute_total_quotation_and_sale_orders_and_sale_order_amount(self):
        sale_orders = self.env['sale.order'].search(
            ['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_id.child_ids.ids)])
        total_quotation = 0
        total_sale_order = 0
        total_sale_order_amount = 0
        for sale_order in sale_orders:
            if sale_order.state == 'draft':
                total_quotation += 1
            elif sale_order.state == 'sale':
                total_sale_order += 1
                total_sale_order_amount += sale_order.amount_total

        self.total_quotation = total_quotation
        self.total_sales_orders = total_sale_order
        self.total_sale_order_amount = total_sale_order_amount

    def _compute_percentage_of_conversion(self):
        for lead_count_line in self:
            if lead_count_line.total_revenue > 0:
                lead_count_line.percentage_of_conversion = (
                    lead_count_line.total_sale_order_amount / lead_count_line.total_revenue) * 100
            else:
                lead_count_line.percentage_of_conversion = 0

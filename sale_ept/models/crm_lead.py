from odoo.exceptions import ValidationError

from odoo import fields, models, _


class CrmLeadEpt(models.Model):
    _name = "crm.lead.ept2"
    _description = "To manage the crm lead data"

    name = fields.Char(string="Customer Name", required=True, help="Enter customer name")
    email = fields.Char(string="Email", required=True, help="Enter email")
    phone = fields.Char(string="Phone", required=True, help="Enter phone")
    expected_revenue = fields.Float(string="Expected Revenue", digits=(6, 3),
                                    help="Enter expected revenue")
    sales_person = fields.Char(string="SalesPerson", required=True, help="Enter sales person")
    sales_team = fields.Char(string="SalesTeam", help="Enter sales team")
    campaign = fields.Char(string="Campaign", help="Enter campaign")
    channel = fields.Selection(selection=[
        ('Facebook', 'Facebook'),
        ('WhatsApp', 'WhatsApp'),
        ('Email', 'Email'),
        ('Newspaper', 'Newspaper'),
        ('Television', 'Television'),
        ('Phone Call', 'Phone Call'),
        ('SMS', 'SMS'),
        ('Google Ads', 'Google Ads')
    ], string="Channel", required=True, help="Select channel")
    state = fields.Selection(selection=[
        ('New', 'New'),
        ('Qualified', 'Qualified'),
        ('Proposition', 'Proposition'),
        ('Won', 'Won'),
        ('Lost', 'Lost')
    ], string="State", help="Select state", default="New")
    next_follow_up_date = fields.Date(string="Next Followup Date", required=True,
                                      help="Enter next follow up date")
    won_date = fields.Date(string="Won Date", help="Enter won date")
    lost_reason = fields.Text(string="Lost Reason", help="Enter lost reason")
    partner_id = fields.Many2one(string="Partner", help="Partner id",
                                 comodel_name="res.partner.ept4", readonly=True)
    order_ids = fields.One2many(string="Orders", help="Order ids",
                                comodel_name="sale.order.line.ept4",
                                inverse_name="order_id")
    lead_line_ids = fields.One2many(string="Lead Line", help="Lead line ids",
                                    comodel_name="crm.lead.line.ept",
                                    inverse_name="lead_id")

    def mark_as_won(self):
        self.state = 'Won'

    def mark_as_lost(self):
        self.state = 'Lost'

    def prepare_sales_quotation(self):
        customer_id = self.partner_id.id
        invoices = self.partner_id.child_ids.filtered(
            lambda child_id: child_id.address_type == 'Invoice')
        shippings = self.partner_id.child_ids.filtered(
            lambda child_id: child_id.address_type == 'Shipping')
        invoice_id = invoices[0].id if invoices else False
        shipping_id = shippings[0].id if shippings else False
        if invoice_id is False or shipping_id is False:
            raise ValidationError(_("Either customer invoice or shipping address is missing."))
        order_date = fields.Date.today()
        salesperson_id = self.env.uid
        order_lines = []
        for lead_line in self.lead_line_ids:
            name = lead_line.product_id.name
            product_price = lead_line.product_id.sale_price
            order_lines.append((0, 0, {
                'product_id': lead_line.product_id.id,
                'quantity': lead_line.expected_sell_qty,
                'uom_id': lead_line.uom_id.id,
                'name': name,
                'unit_price': product_price
            }))
        quotation = {
            'invoice_id': invoice_id,
            'shipping_id': shipping_id,
            'sale_order_date': order_date,
            'customer_id': customer_id,
            'order_line_ids': order_lines,
            'lead_id': self.id,
            'salesperson_id': salesperson_id
        }
        return quotation

    def generate_sales_quotation(self):
        if self.partner_id:
            sale_quotation_vals = self.prepare_sales_quotation()
            sale_quotation = self.env['sale.order.ept4'].create(sale_quotation_vals)
            return sale_quotation
        else:
            raise ValidationError(_("No customer found, create new customer."))

    def prepare_customer(self):
        customer_details = {
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }
        return customer_details

    def create_customer(self):
        customer_vals = self.prepare_customer()
        created_customer = self.env['res.partner.ept4'].create(customer_vals)
        self.partner_id = created_customer.id

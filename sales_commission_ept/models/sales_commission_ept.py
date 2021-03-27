from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SalesCommissionEpt(models.Model):
    _name = "sales.commission.ept"
    _description = "To store sales commission related data"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Commission Name", help="Commission name sequential", readonly=True,
                       copy=False)
    user_id = fields.Many2one(string="User", help="User id", comodel_name="res.users")
    from_date = fields.Date(string="From the date", help="From date", required=True)
    to_date = fields.Date(string="To the date", help="To date", required=True)
    paid_date = fields.Date(string="Date of paid", help="Paid date")
    total_commission = fields.Float(string="Total commissions", help="Total commission",
                                    digits=(6, 2), compute="_compute_total_commission")
    status = fields.Selection(selection=[
        ('Draft', 'Draft'),
        ('Paid', 'Paid')
    ], string="Commission Status", help="Status", default="Draft", tracking=True)
    commission_lines_ids = fields.One2many(string="Commissions", help="Commission line ids",
                                           comodel_name="sales.commission.line",
                                           inverse_name="sale_commission_id")
    product_id = fields.Many2one(string="Product", help="Product id",
                                 comodel_name="product.product")

    @api.model
    def create(self, val):
        """
        To generate the unique name for the sales commission and to restrict creating those record
        whose from date and to date is in the range of existing user's from date and to date.
        :param val:
        :return: new unique name for the sales commission
        """
        sales_commissions = self.env['sales.commission.ept'].search(
            [('user_id', '=', val.get('user_id'))]).filtered_domain(
                [('from_date', '<', val.get('from_date')), ('to_date', '>', val.get('to_date'))])
        if sales_commissions:
            raise ValidationError(_("Same user with conflicting date can't be created."))
        val['name'] = self.env['ir.sequence'].next_by_code('sales.commission.ept')
        return super(SalesCommissionEpt, self).create(val)

    def default_get(self, fields):
        # To set the default product from ir.config_parameter model
        # returns - dictionary of fields with default value
        default = super(SalesCommissionEpt, self).default_get(fields)
        default['product_id'] = int(self.env[
            'ir.config_parameter'].sudo().get_param(
                'sales_commission_ept.commission_product_id'))

        return default

    def _compute_total_commission(self):
        # computes the total commission from the commission lines
        # returns -
        total_commission = 0.0
        for commission in self.commission_lines_ids:
            total_commission += commission.amount

        self.total_commission = total_commission

    def calculate_commission_using_percentage(self, amount_total):
        """
        Fetches the percentage of the commission and using that calculates the actual commission
        :return: amount of the calculated commission
        """
        individual_commission_percentage = float(self.env['ir.config_parameter'].sudo().get_param(
            'sales_commission_ept.individual_commission_percentage'))
        return (amount_total * individual_commission_percentage) / 100

    def calculate_commission(self):
        """
        Generates a line in commission lines from sale order and calculates the commission using the
        given percentage of commission.
        If there are already lines available, deletes those lines first and then generates new lines
        :return:
        """
        if self.commission_lines_ids:
            for commission in self.commission_lines_ids:
                commission.unlink()

        orders = self.env['sale.order'].search([('user_id', '=', self.user_id.id)])
        commission_lines = []
        for order in orders:
            commission_lines.append((0, 0, {
                'commission_date': order.date_order,
                'source_document': order.name,
                'amount': self.calculate_commission_using_percentage(order.amount_total),
                'user_id': self.user_id.id,
                'partner_id': order.partner_id.id,
                'is_paid_amount': False
            }))

        self.commission_lines_ids = commission_lines

    def paid_commission(self):
        """
        To mark all line records as paid and update commission record status as paid.
        Also sets the current date as paid date and state as paid
        :return: -
        """
        commission_lines = self.env['sales.commission.ept'].browse(
            self.id).commission_lines_ids
        for commission in commission_lines:
            commission.is_paid_amount = True
            commission.status = 'Paid'

        self.paid_date = fields.Date.today()
        self.status = 'Paid'

    def reset_to_draft(self):
        # Opens the wizard to enter the reason for re-setting to draft state
        # returns - dictionary of action
        return self.env['ir.actions.act_window']._for_xml_id(
            "sales_commission_ept.action_reset_draft_message_wizard")

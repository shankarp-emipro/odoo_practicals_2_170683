from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    crm_lead_id = fields.Many2one(string="CRM Lead", help="Crm lead id", comodel_name="crm.lead")
    order_profit_margin = fields.Float(string="Profit margin",
                                       help="Profit margin - percentage of the profit",
                                       digits=(6, 2),
                                       compute="_compute_order_profit_value_margin")
    order_profit_value = fields.Float(string="Profit value",
                                      help="Profit value (cost_price - unit_price)", digits=(6, 2),
                                      compute="_compute_order_profit_value_margin")
    product_tmpl_ids = fields.Many2many(string="Product Template", help="Product template ids",
                                        comodel_name="product.template")
    is_all_picking_completed = fields.Boolean(string="All picking completed",
                                              help="Is all picking completed",
                                              compute="_compute_is_all_picking_completed",
                                              search="_search_is_all_picking_completed")

    def _compute_is_all_picking_completed(self):
        # Checks the state of all pickings of all sale order and if any picking state is false then
        # assigns the is_all_picking_completed to false otherwise true
        # returns -
        for order in self:
            if False not in order.picking_ids.mapped(
                    lambda picking: picking.state == 'done' or picking.state == 'cancel'):
                order.is_all_picking_completed = True
            else:
                order.is_all_picking_completed = False

    def _search_is_all_picking_completed(self, operator, value):
        # When "completed picking" filter is applied then this method is called and list of
        # sale orders are gathered of which stock picking state is either cancel or done.
        # returns - returns the list of id of the sale_order.
        # TODO: This can be achieved by sql query
        # query = "select s.sale_id from (select sale_id from stock_picking where sale_id is not" \
        #         " NULL) as s join stock_picking" \
        #         " as p on s.sale_id = p.id where p.state in ('done','cancel')"
        # self.env.cr.execute(query)
        # sale_orders = self.env.cr.fetchall()

        sale_orders = []
        for order in self.env['sale.order'].search([('picking_ids', '!=', False)]):
            if not order.picking_ids.filtered(
                    lambda picking: picking.state not in ['done', 'cancel']):
                sale_orders.append(order.id)
        return [('id', 'in', sale_orders)]

    @api.onchange('product_tmpl_ids')
    def _onchange_product_template(self):
        # When the product template is changed product variants of that template is set in
        # oder line
        # :returns -
        for template in self.product_tmpl_ids:
            for p_variant in template.product_variant_ids:
                if p_variant.id.origin not in self.order_line.product_id.ids:
                    for variant in template.product_variant_ids:
                        self.write({
                            'order_line': [(0, 0, {
                                'name': variant.name,
                                'price_unit': variant.lst_price,
                                'product_uom_qty': 1.0,
                                'customer_lead': 0.0,
                                'product_id': variant.id.origin
                            })]
                        })

        # templates = self.product_tmpl_ids.ids
        # for product in self.order_line.product_id:
        #     if product.product_tmpl_id.id not in templates:
        #         order = self.env['sale.order.line'].search([('order_id', '=', self.id)])
        #         order.order_line.product_id

    def _compute_order_profit_value_margin(self):
        # To calculate the order profit value and margin
        # returns -
        order_profit_value = 0
        for line in self.order_line:
            order_profit_value += line.profit_value

        self.order_profit_value = order_profit_value
        if self.amount_untaxed > 0:
            self.order_profit_margin = (order_profit_value / self.amount_untaxed) * 100
        else:
            self.order_profit_margin = 0.0

    def manage_deposits(self):
        """
        When “Manage Deposits” button is clicked, scan all the products and check if there is any
        deposit product associated with the product. If there is any, then that product should be
        added to the sale.order.line. If once the deposit product is added already, then it should
        not be added more than once.

        If the quantity of main product is updated, make sure to update the quantity of deposit
        product also
        :return: -
        """
        for line in self.order_line:
            if line.product_id.deposit_product_id:
                if line.child_ids:
                    vals = {
                        'product_uom_qty': line.product_uom_qty * line.product_id.deposit_product_qty,
                    }
                    line.child_ids.write(vals)
                else:
                    vals = {
                        'parent_line_id': line.id,
                        'product_id': line.product_id.deposit_product_id.id,
                        'name': line.product_id.deposit_product_id.name,
                        'product_uom_qty': line.product_uom_qty * line.product_id.deposit_product_qty,
                        'price_unit': line.product_id.deposit_product_id.lst_price,
                        'tax_id': line.product_id.deposit_product_id.taxes_id.ids,
                        'order_id': self.id
                    }
                    self.env['sale.order.line'].create(vals)

    def action_confirm(self):
        # While confirming the sale order the delivery product's id is fetched from the system
        # parameters and set in the order line.
        # returns -
        super(SaleOrder, self).action_confirm()
        product_id = int(
            self.env['ir.config_parameter'].sudo().get_param('sale.default_product_id'))
        if product_id not in list(map(lambda line: line.product_id.id, self.order_line)):
            self.write({
                'order_line': [(0, 0, {
                    'product_id': product_id
                })]
            })

    def my_message(self):
        # To generate the message in chatter section on click of the button
        # returns -
        message = self.message_post()
        message['body'] = "Sale order no: " + self.name
        return message

    def update_salesperson_salesteam(self):
        # To open a wizard for updating the sales info
        # returns -
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "sale_order_extended.action_sales_info_update")
        action['context'] = {'default_user_id': self.user_id.id, 'default_team_id': self.team_id.id,
                             'default_user_new_id': self.user_id.id,
                             'default_team_new_id': self.user_id.sale_team_id.id}
        return action

    def get_order_lines(self):
        # To get the order lines of all the sale order which are reserved in stock picking
        # returns - action of list view of sale.order.line
        products = self.order_line.product_id.ids

        orders_lines = self.env['sale.order.line'].search([('product_id', 'in', products)]).ids

        moves = self.env['stock.move'].search(
            [('sale_line_id', 'in', orders_lines), ('state', '=', 'assigned'),
             ('state', 'not in', ['cancel', 'done'])])

        action = self.env['ir.actions.act_window']._for_xml_id(
            "sale_order_extended.action_view_sale_order_lines")

        action['domain'] = [('id', 'in', moves.sale_line_id.ids)]
        return action

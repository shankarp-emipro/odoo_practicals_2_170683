from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "sale.order.ept4"
    _description = "To store sale order"

    name = fields.Char(string="Order No", help="Enter order no", readonly=True, copy=False)
    customer_id = fields.Many2one(string="Customer", help="Customer id",
                                  comodel_name="res.partner.ept4", tracking=True)
    invoice_id = fields.Many2one(string="Invoice", help="Invoice id",
                                 comodel_name="res.partner.ept4")
    shipping_id = fields.Many2one(string="Shipping", help="Shipping id",
                                  comodel_name="res.partner.ept4")
    sale_order_date = fields.Date(string="Sale-order date", help="Enter sale order date")
    order_line_ids = fields.One2many(string="Order line", help="Order line ids",
                                     comodel_name="sale.order.line.ept4",
                                     inverse_name="order_id")
    salesperson_id = fields.Many2one(string="Salesperson", help="Salesperson id",
                                     comodel_name="res.users")
    state = fields.Selection(selection=[
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string="State", help="Select sate", default='Draft')
    total_weight = fields.Float(string="Total weight", help="Total weight of products",
                                digits=(6, 2),
                                compute="_compute_total_weight_and_volume_nostore")
    total_volume = fields.Float(string="Total volume", help="Total volume of products",
                                digits=(6, 2),
                                compute="_compute_total_weight_and_volume_nostore")
    order_total = fields.Float(string="Order total", help="Total of order",
                               compute="_compute_order_total", store=True)
    lead_id = fields.Many2one(string="Lead", help="Lead id", comodel_name="crm.lead.ept2")
    warehouse_id = fields.Many2one(string="Warehouse", help="Warehouse id",
                                   comodel_name="stock.warehouse.ept")
    picking_ids = fields.One2many(string="Picking", help="Picking ids",
                                  comodel_name="stock.picking.ept",
                                  inverse_name="sale_order_id", readonly=True)
    count_stock_picking = fields.Integer(string="Picking count", help="Count stock picking",
                                         compute="_compute_count_stock_picking_and_stock_move")
    count_stock_move = fields.Integer(string="Stock move count", help="Count stock move",
                                      compute="_compute_count_stock_picking_and_stock_move")
    total_tax = fields.Float(string="Tax total", help="Sum of all the tax of the sale order line",
                             digits=(6, 2), compute="_compute_total_tax", store=True)
    total_amount = fields.Float(string="Amount total",
                                help="Sum of subtotal without tax and total tax",
                                digits=(6, 2), compute="_compute_total_amount", store=True)
    total_untaxed_amount = fields.Float(string="Untaxed Amount",
                                        help="Sum of all the untaxed amounts",
                                        digits=(6, 2), compute="_compute_total_amount", store=True)

    @api.depends('order_line_ids.subtotal_tax')
    def _compute_total_tax(self):
        total_tax = 0
        total_amount = 0
        total_untaxed_amount = 0
        for order_line in self.order_line_ids:
            total_tax += order_line.subtotal_tax - order_line.subtotal_without_tax
            total_amount += order_line.subtotal_tax
            total_untaxed_amount += order_line.subtotal_without_tax

        self.total_tax = total_tax
        self.total_amount = total_amount
        self.total_untaxed_amount = total_untaxed_amount

    @api.model_create_multi
    def create(self, vals):
        # To generate unique sale order number
        # this is achieved by invoking the next_by_code() method of ir.sequence model
        # returns - record
        record = None
        for val in vals:
            val['name'] = self.env['ir.sequence'].next_by_code('sale.order.ept4')
            record = super(SaleOrder, self).create(val)
        return record

    def write(self, vals):
        # To perform any business logics before write the data in database
        # returns - boolean as a flag
        bool_flag = super(SaleOrder, self).write(vals)
        return bool_flag

    def unlink(self):
        # To perform any business logics before delete the data from database
        # returns - super call to the delete method of the core code
        return super(SaleOrder, self).unlink()

    def copy(self, default=None):
        # To perform any business logics before copy the data from database
        # default parameter is used to overwrite specified column value in a record
        # returns - super call to the delete method of the core code
        default = {}
        default.update({'sale_order_date': fields.date.today()})
        return super(SaleOrder, self).copy(default)

    @api.onchange('customer_id')
    def _onchange_customer(self):
        """
        When customer id will be changed then invoice id and shipping id will be set accordingly.
        :returns -
        """
        invoices = self.customer_id.child_ids.filtered(
            lambda child_id: child_id.address_type == 'Invoice')
        shippings = self.customer_id.child_ids.filtered(
            lambda child_id: child_id.address_type == 'Shipping')
        self.invoice_id = invoices[0] if invoices else False
        self.shipping_id = shippings[0] if shippings else False

    def _compute_total_weight_and_volume_nostore(self):
        # to compute the total weight and volume of products, the data will not be stored
        # in database
        # returns -
        for sale_order in self:
            total_weight = 0
            total_volume = 0
            for product in sale_order.order_line_ids:
                total_weight += product.quantity * product.product_id.weight
                total_volume += product.quantity * product.product_id.volume
            sale_order.total_weight = total_weight
            sale_order.total_volume = total_volume

    @api.depends('order_line_ids.subtotal_without_tax')
    def _compute_order_total(self):
        # to compute the total of all subtotal, the result will be stored in the database
        # returns -
        for data2 in self:
            temp_order_total = 0
            for data in data2.order_line_ids:
                temp_order_total += data.subtotal_without_tax
            data2.order_total = temp_order_total

    # def prepare_stock_move(self):
    #     # prepares the stock move to add in stock move line
    #     # returns - dictionary
    #     stock_move_line = []
    #     source_location = self.warehouse_id.stock_location_id.id
    #     destination_location = self.env['stock.location.ept'].search([('location_type', '=', 'Customer')], limit=1)
    #     for order_line in self.order_line_ids:
    #         name = order_line.product_id.name
    #         product_id = order_line.product_id.id
    #         uom_id = order_line.uom_id.id
    #         qty_to_deliver = order_line.quantity
    #         state = 'Draft'
    #         sale_line_id = order_line.id
    #
    #         stock_move_line.append((0, 0, {
    #             'name': name,
    #             'product_id': product_id,
    #             'uom_id': uom_id,
    #             'source_location_id': source_location,
    #             'destination_location_id': destination_location.id if destination_location else False,
    #             'qty_to_deliver': qty_to_deliver,
    #             'state': state,
    #             'sale_line_id': sale_line_id
    #         }))
    #         order_line.write({'state': 'Confirmed'})
    #
    #     return stock_move_line
    #
    # def prepare_stock_picking(self):
    #     # prepare stock picking dictionary
    #     # return - dictionary
    #     vals = {
    #         'partner_id': self.shipping_id.id,
    #         'sale_order_id': self.id,
    #         'stock_move_ids': self.prepare_stock_move()
    #     }
    #     return vals
    #
    # def generate_stock_picking(self):
    #     # generates the stock picking
    #     # returns -
    #     stock_picking_vals = self.prepare_stock_picking()
    #     self.env['stock.picking.ept'].create(stock_picking_vals)
    #
    # def confirm_order(self):
    # to confirm the order, which changes the state of current order and order line to 'Confirmed'
    #     # returns -
    #     self.generate_stock_picking()
    #     self.state = 'Confirmed'

    def prepare_stock_move(self, warehouse, order_lines):
        # prepares the stock move to add in stock move line
        # returns - dictionary
        stock_move_line = []
        source_location = warehouse.stock_location_id.id
        destination_location = self.env['stock.location.ept'].search(
            [('location_type', '=', 'Customer')], limit=1)
        for order_line in order_lines:
            name = order_line.product_id.name
            product_id = order_line.product_id.id
            uom_id = order_line.uom_id.id
            qty_to_deliver = order_line.quantity
            state = 'Draft'
            sale_line_id = order_line.id

            stock_move_line.append((0, 0, {
                'name': name,
                'product_id': product_id,
                'uom_id': uom_id,
                'source_location_id': source_location,
                'destination_location_id': destination_location.id if destination_location else False,
                'qty_to_deliver': qty_to_deliver,
                'state': state,
                'sale_line_id': sale_line_id
            }))
            order_line.write({'state': 'Confirmed'})

        return stock_move_line

    def prepare_stock_picking(self, warehouse, order_lines):
        # prepare stock picking dictionary
        # return - dictionary
        vals = {
            'partner_id': self.shipping_id.id,
            'sale_order_id': self.id,
            'stock_move_ids': self.prepare_stock_move(warehouse, order_lines)
        }
        return vals

    def generate_stock_picking(self, order_line_group_by_warehouse):
        # generates the stock picking
        # returns -
        for warehouse, order_lines in order_line_group_by_warehouse.items():
            stock_picking_vals = self.prepare_stock_picking(warehouse, order_lines)
            self.env['stock.picking.ept'].create(stock_picking_vals)

    def confirm_order(self):
        # to confirm the order, which changes the state of current order and order line
        # to 'Confirmed'
        # returns -
        order_line_group_by_warehouse = {self.warehouse_id: []}
        for order_line in self.order_line_ids:
            if order_line.warehouse_id.id:
                if order_line.warehouse_id.id not in order_line_group_by_warehouse.keys():
                    order_line_group_by_warehouse.update({
                        order_line.warehouse_id: [order_line]
                    })
                else:
                    order_line_group_by_warehouse.get(order_line.warehouse_id).append(order_line)
            else:
                order_line_group_by_warehouse.get(self.warehouse_id).append(order_line)

        self.generate_stock_picking(order_line_group_by_warehouse)
        self.state = 'Confirmed'

    def _compute_count_stock_picking_and_stock_move(self):
        # To display the count of the total delivery order and total stock move
        # returns -
        self.count_stock_picking = len(self.picking_ids.ids)

    def view_delivery_order(self):
        """
        To list out the delivery order(stock picking) of particular sale order. If there is only one
        delivery order then form view will be returned otherwise tree view will be returned.
        :return: action
        """
        action = {
            'name': 'Stock Picking',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking.ept',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)]
        }
        picking_ids = self.picking_ids.ids
        if len(picking_ids) == 1:
            action['views'] = [(self.env.ref('sale_ept.view_stock_picking_form').id, 'form')]
            action['res_id'] = picking_ids[0]
        return action

    def view_stock_move(self):
        """
        To list out the stock move of particular sale order. If there is only
        one stock move then form view will be loaded otherwise tree view will be loaded.
        :return: action
        """
        action = {
            'name': 'Stock Move',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move.ept',
            'view_mode': 'tree,form'
        }
        stock_move_ids = self.picking_ids.stock_move_ids.ids
        if len(stock_move_ids) == 1:
            action['views'] = [(self.env.ref('sale_ept.view_stock_move_form').id, 'form')]
            action['res_id'] = stock_move_ids[0]
        else:
            view_id = self.env.ref('sale_ept.view_stock_move_tree').id
            action['views'] = [(view_id, 'tree'),
                               (self.env.ref('sale_ept.view_stock_move_form').id, 'form')]
            action['domain'] = [('picking_id.sale_order_id', '=', self.id)]
        return action

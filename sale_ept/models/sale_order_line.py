from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _name = "sale.order.line.ept4"
    _description = "To store sale order line"

    name = fields.Text(string="Description", help="Description about the item to be sold")
    order_id = fields.Many2one(string="Order no", help="Order no", comodel_name="sale.order.ept4")
    product_id = fields.Many2one(string="Product", help="Product id", comodel_name="product.ept4")
    quantity = fields.Float(string="Qty", help="Enter quantity", digits=(6, 2))
    unit_price = fields.Float(string="Unit price", help="Enter unit price", digits=(6, 2))
    state = fields.Selection(selection=[
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ], string="State", help="Select state", default="Draft")
    uom_id = fields.Many2one(string="UOM", help="UOM id", comodel_name="product.uom.ept4")

    subtotal_without_tax = fields.Float(string="Untaxed subtotal",
                                        help="Calculates the subtotal of products",
                                        compute="_compute_subtotal_without_tax", store=True)
    stock_move_ids = fields.One2many(string="Stock Move", help="Stock move ids",
                                     comodel_name="stock.move.ept",
                                     inverse_name="sale_line_id")
    delivered_qty = fields.Float(string="Qty delivered",
                                 help="Sum of all the delivered order qty which are validated",
                                 compute="_compute_delivered_qty")
    warehouse_id = fields.Many2one(string="Warehouse", help="Warehouse id",
                                   comodel_name="stock.warehouse.ept")
    tax_ids = fields.Many2many(string="Customer Taxes", help="Customer taxes",
                               comodel_name="account.tax.ept")
    subtotal_tax = fields.Float(string="Subtotal of Tax", help="Subtotal tax", digits=(6, 2),
                                compute="_compute_subtotal_tax", store=True)

    @api.depends('quantity', 'unit_price', 'tax_ids')
    def _compute_subtotal_tax(self):
        for order_line in self:
            tax_amount = 0
            for tax in order_line.tax_ids:
                if tax.tax_amount_type == 'Fixed':
                    tax_amount += tax.tax_value
                elif tax.tax_amount_type == 'Percentage':
                    tax_amount += (order_line.subtotal_without_tax * tax.tax_value) / 100

            order_line.subtotal_tax = order_line.subtotal_without_tax + tax_amount

    @api.onchange('product_id')
    def _onchange_product(self):
        # to auto select unit price when the product is selected
        # returns -
        self.quantity = 1
        self.unit_price = self.product_id.sale_price
        self.uom_id = self.product_id.uom_id
        self.tax_ids = self.product_id.tax_ids

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal_without_tax(self):
        # subtotal without tax of the products is calculated based on quantity and unit price
        # returns -
        for data in self:
            data.subtotal_without_tax = data.quantity * data.unit_price

    def _compute_delivered_qty(self):
        # computes the delivered qty
        # returns -
        for line in self:
            total_delivered_qty = 0
            for stock_move in line.stock_move_ids:
                if stock_move.picking_id.state == 'Validate':
                    total_delivered_qty += stock_move.qty_delivered
            line.delivered_qty = total_delivered_qty

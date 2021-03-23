from odoo import fields, models, api


class StockPicking(models.Model):
    _name = "stock.picking.ept"
    _description = "To store stock picking data"

    name = fields.Char(string="Picking Order", help="Picking order", readonly=True, copy=False)
    partner_id = fields.Many2one(string="Partner", help="Partner id",
                                 comodel_name="res.partner.ept4")
    back_order_id = fields.Many2one(string="Back Order", help="Back order id",
                                    comodel_name="stock.picking.ept")
    state = fields.Selection(selection=[
        ('Draft', 'Draft'),
        ('Validate', 'Validate'),
        ('Cancelled', 'Cancelled')
    ], string="State", help="Select state of the stock picking", default="Draft")
    sale_order_id = fields.Many2one(string="Sale Order", help="Sale order id",
                                    comodel_name="sale.order.ept4")
    stock_move_ids = fields.One2many(string="Stock Move", help="Stock move ids",
                                     comodel_name="stock.move.ept",
                                     inverse_name="picking_id")
    parent_picking_id = fields.Many2one(string="Parent Picking", help="Parent picking id",
                                        comodel_name="stock.picking.ept")

    @api.model_create_multi
    def create(self, vals):
        # To generate unique stock picking number
        # this is achieved by invoking the next_by_code() method of ir.sequence model
        # returns - record
        record = None
        for val in vals:
            val['name'] = self.env['ir.sequence'].next_by_code('stock.picking.ept')
            record = super(StockPicking, self).create(val)
        return record

    def validate_stock_picking(self):
        # if qty_delivered is less than qty_to_deliver then creates back order for that stock move
        # returns -
        # need_back_order is the flag to restrict generating multiple back order at a time
        need_back_order = True
        # back_order_record is newly created back order record which is used to relate the
        # stock move
        back_order_record = None
        for stock_move in self.stock_move_ids:
            stock_move.state = 'Done'
            if stock_move.qty_delivered < stock_move.qty_to_deliver:
                if need_back_order:
                    back_order_record = self.env['stock.picking.ept'].create({
                        'partner_id': self.partner_id.id,
                        'back_order_id': self.id,
                        'sale_order_id': self.sale_order_id.id
                    })
                    need_back_order = False

                self.env['stock.move.ept'].create({
                    'name': stock_move.name,
                    'product_id': stock_move.product_id.id,
                    'uom_id': stock_move.uom_id.id,
                    'source_location_id': stock_move.source_location_id.id,
                    'destination_location_id': stock_move.destination_location_id.id,
                    'qty_to_deliver': stock_move.qty_to_deliver - stock_move.qty_delivered,
                    'sale_line_id': stock_move.sale_line_id.id,
                    'picking_id': back_order_record.id
                })
        self.state = 'Validate'

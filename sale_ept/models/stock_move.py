from odoo import fields, models


class StockMove(models.Model):
    _name = "stock.move.ept"
    _description = "To store the stock move data"

    name = fields.Char(string="Description", help="Enter product name")
    product_id = fields.Many2one(string="Product", help="Product id", comodel_name="product.ept4",
                                 required=True)
    uom_id = fields.Many2one(string="UOM", help="UOM id", comodel_name="product.uom.ept4",
                             required=True)
    source_location_id = fields.Many2one(string="Source Location", help="Source location id",
                                         comodel_name="stock.location.ept")
    destination_location_id = fields.Many2one(string="Destination Location",
                                              help="Destination location id",
                                              comodel_name="stock.location.ept")
    qty_to_deliver = fields.Float(string="Qty to-deliver", help="Enter qty to deliver")
    qty_delivered = fields.Float(string="Qty-delivered", help="Enter delivered qty")
    state = fields.Selection(selection=[
        ('Draft', 'Draft'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string="State", help="Select state of the stock move", default="Draft")
    sale_line_id = fields.Many2one(string="Sale Line", help="Sale line id",
                                   comodel_name="sale.order.line.ept4")
    stock_inventory_id = fields.Many2one(string="Stock Inventory", help="Stock inventory id",
                                         comodel_name="stock.inventory.ept")
    picking_id = fields.Many2one(string="Picking", help="Picking id",
                                 comodel_name="stock.picking.ept")

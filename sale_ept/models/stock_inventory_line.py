from odoo import fields, models


class StockInventoryLine(models.Model):
    _name = "stock.inventory.line.ept"
    _description = "To store the stock inventory data"

    product_id = fields.Many2one(string="Product", help="Product id", comodel_name="product.ept4")
    available_qty = fields.Float(string="Qty Available", help="Enter available qty")
    counted_product_qty = fields.Float(string="Counted Qty",
                                       help="Enter counted product qty")
    difference = fields.Float(string="Stock difference", help="Enter difference",
                              compute="_compute_difference")
    inventory_id = fields.Many2one(string="Inventory", help="Inventory id",
                                   comodel_name="stock.inventory.ept",
                                   ondelete="cascade")

    def _compute_difference(self):
        # computes the difference of the counted stock and the avail
        for stock_move in self:
            stock_move.difference = stock_move.counted_product_qty - stock_move.available_qty

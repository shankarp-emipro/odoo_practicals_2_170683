from odoo import fields, models


class StockInventory(models.Model):
    _name = "stock.inventory.ept"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "To store the stock inventroy data"

    name = fields.Char(string="Stock Inventory", help="Enter stock inventory name")
    state = fields.Selection(selection=[
        ('Draft', 'Draft'),
        ('In-Progress', 'In-Progress'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    ], string="State", help="Select state of stock inventory", default='Draft')
    location_id = fields.Many2one(string="Location", help="Location id",
                                  comodel_name="stock.location.ept")
    inventory_date = fields.Date(string="Inventory-Date", help="Inventory date",
                                 default=fields.Date.today())
    inventory_line_ids = fields.One2many(string="Inventory Line", help="Inventory line ids",
                                         comodel_name="stock.inventory.line.ept",
                                         inverse_name="inventory_id")
    stock_move_ids = fields.One2many(string="Stock Move", help="Stock move ids",
                                     comodel_name="stock.move.ept",
                                     inverse_name="stock_inventory_id")

    def start_inventory(self):
        # passes the location id as a context to find the particular stock location's stock count
        # returns -
        for inventory_line in self.inventory_line_ids:
            inventory_line.available_qty = inventory_line.product_id.with_context(
                {'location_id': self.location_id.id}).product_stock
        self.state = 'In-Progress'

    def validate_inventory(self):
        # validates the inventory and moves the stock from inventory loss location to the
        # stock location
        # returns -
        inventory_loss_location = self.env['stock.location.ept'].search(
            [('location_type', '=', 'Inventory Loss'), ('is_scrap_location', '=', False)], limit=1)
        for inventory_line in self.inventory_line_ids:
            self.env['stock.move.ept'].create({
                'name': inventory_line.product_id.name,
                'product_id': inventory_line.product_id.id,
                'uom_id': inventory_line.product_id.uom_id.id,
                'source_location_id': inventory_loss_location.id if inventory_loss_location else False,
                'destination_location_id': self.location_id.id,
                'qty_to_deliver': inventory_line.difference,
                'qty_delivered': inventory_line.difference,
                'state': 'Done',
                'stock_inventory_id': self.id
            })

        self.state = 'Done'

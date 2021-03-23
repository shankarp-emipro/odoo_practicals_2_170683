from odoo import fields, models, api


class StockInventoryLine(models.TransientModel):
    _name = "product.stock.update.ept"
    _description = "Wizard to update product stock"

    location_id = fields.Many2one(string="Location", help="Location id", comodel_name="stock.location.ept")
    current_stock = fields.Float(string="Available stock", help="Current stock", digits=(6, 2))
    counted_qty = fields.Float(string="Qty counted", help="Counted qty", digits=(6, 2))
    difference_qty = fields.Float(string="Qty difference", help="Difference qty", digits=(6, 2),
                                  compute="_compute_difference_qty")

    @api.onchange('location_id')
    def get_current_stock(self):
        if self.location_id:
            products = self.env['product.ept4'].browse(self._context.get('active_ids'))
            for product in products:
                self.current_stock = product.with_context(location_id=self.location_id.id).product_stock

    @api.depends('counted_qty', 'current_stock')
    def _compute_difference_qty(self):
        self.difference_qty = self.counted_qty - self.current_stock

    def prepare_stock_inventory(self):
        product_name = self.env['product.ept4'].browse(self._context.get('active_id')).name
        stock_inventory_vals = {
            'name': 'Inventory: ' + product_name,
            'location_id': self.location_id.id,
            'state': 'Done'
        }
        return stock_inventory_vals

    def create_stock_inventory(self):
        vals = self.prepare_stock_inventory()
        return self.env['stock.inventory.ept'].create(vals)

    def prepare_stock_inventory_line(self, inventory_id):
        product = self.env['product.ept4'].browse(self._context.get('active_id'))
        available_qty = product.with_context(
            location_id=self.location_id.id).product_stock
        stock_inventory_line_vals = {
            'product_id': product.id,
            'available_qty': available_qty,
            'counted_product_qty': self.counted_qty,
            'difference': self.difference_qty,
            'inventory_id': inventory_id
        }
        return stock_inventory_line_vals

    def create_stock_inventory_line(self, inventory_id):
        vals = self.prepare_stock_inventory_line(inventory_id)
        return self.env['stock.inventory.line.ept'].create(vals)

    def validate_inventory(self, inventory_line, inventory_id):
        inventory_loss_location = self.env['stock.location.ept'].search(
            [('location_type', '=', 'Inventory Loss'), ('is_scrap_location', '=', False)], limit=1)
        self.env['stock.move.ept'].create({
            'name': inventory_line.product_id.name,
            'product_id': inventory_line.product_id.id,
            'uom_id': inventory_line.product_id.uom_id.id,
            'source_location_id': inventory_loss_location.id if inventory_loss_location else False,
            'destination_location_id': self.location_id.id,
            'qty_to_deliver': inventory_line.difference,
            'qty_delivered': inventory_line.difference,
            'state': 'Done',
            'stock_inventory_id': inventory_id
        })

    def update_stock(self):
        inventory_id = self.create_stock_inventory()
        inventory_line = self.create_stock_inventory_line(inventory_id.id)
        self.validate_inventory(inventory_line, inventory_id.id)
        inventory_id.message_post(body="Stock updated.")


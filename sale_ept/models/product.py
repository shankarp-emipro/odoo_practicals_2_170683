from odoo import fields, models


class Product(models.Model):
    _name = "product.ept4"
    _description = "To store products"

    name = fields.Char(string="Product Name", help="Enter product name", required=True)
    sku = fields.Char(string="SKU", help="Enter sku", required=True)
    weight = fields.Float(string="Weight", help="Enter weight", digits=(6, 2))
    length = fields.Float(string="Length", help="Enter length", digits=(6, 2))
    width = fields.Float(string="Width", help="Enter product_width", digits=(6, 2))
    barcode = fields.Char(string="Barcode", help="Enter product_barcode")
    product_type = fields.Selection(selection=[
        ('Storable', 'Storable'),
        ('Consumable', 'Consumable'),
        ('Service', 'Service')
    ], string="Type", help="Select product type")
    sale_price = fields.Float(string="SalePrice", help="Sale price", default="1.00", digits=(6, 2))
    cost_price = fields.Float(string="Cost", help="Cost price", default="1.00", digits=(6, 2))
    product_category_id = fields.Many2one(string="Product category", help="Product category id",
                                          comodel_name="product.category.ept4")
    uom_id = fields.Many2one(string="UOM", help="Uom", comodel_name="product.uom.ept4")
    volume = fields.Float(string="Volume", help="Enter volume", digits=(6, 2))
    product_stock = fields.Float(string="ProductStock", help="Product stock auto computed",
                                 compute="_compute_product_stock")
    tax_ids = fields.Many2many(string="Customer Taxes", help="Customer taxes",
                               comodel_name="account.tax.ept")

    def _compute_product_stock(self):
        # to compute product stock by iterating each warehouse and every stock location of
        # each warehouse
        # returns -
        stock_location_list = self.env['stock.warehouse.ept'].search([]).mapped(
            lambda warehouse: warehouse.stock_location_id.id)
        passed_location_id = self.env.context.get('location_id')
        for product in self:
            product_stock = 0
            if passed_location_id:
                stock_locations_out = self.env['stock.move.ept'].search(
                    [('source_location_id', '=', passed_location_id),
                     ('product_id', '=', product.id)])

                stock_locations_in = self.env['stock.move.ept'].search(
                    [('destination_location_id', '=', passed_location_id),
                     ('product_id', '=', product.id)])
            else:
                stock_locations_out = self.env['stock.move.ept'].search(
                    [('source_location_id', 'in', stock_location_list),
                     ('product_id', '=', product.id)])

                stock_locations_in = self.env['stock.move.ept'].search(
                    [('destination_location_id', 'in', stock_location_list),
                     ('product_id', '=', product.id)])

            for source in stock_locations_out:
                product_stock -= source.qty_delivered

            for destination in stock_locations_in:
                product_stock += destination.qty_delivered

            product.product_stock = product_stock

    def update_stock(self):
        # to update the stock of the product from the wizard on button click
        # returns - dictionary
        view_id = self.env.ref('sale_ept.wizard_form_product_stock_update').id
        return {
            'name': 'Product Stock Update',
            'type': 'ir.actions.act_window',
            'res_model': 'product.stock.update.ept',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'target': 'new'
        }

    def update_stock2(self):
        # to update the stock of the product from the wizard on button click
        # returns - action
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "sale_ept.action_product_stock_update")
        return action

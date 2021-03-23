from odoo import fields, models


class StockWarehouse(models.Model):
    _name = "stock.warehouse.ept"
    _description = "To store stock warehouse data"

    name = fields.Char(string="Warehouse Name", help="Enter warehouse name", required=True)
    short_code = fields.Char(string="Code", help="Short code for warehouse", required=True)
    address = fields.Many2one(string="Warehouse Address", help="Warehouse address",
                              comodel_name="res.partner.ept4")
    stock_location_id = fields.Many2one(string="Stock Location", help="Stock location id",
                                        comodel_name="stock.location.ept",
                                        domain="[('location_type', '=', 'Internal')]")
    view_location_id = fields.Many2one(string="View Location", help="View location id",
                                       comodel_name="stock.location.ept",
                                       domain="[('location_type', '=', 'View')]")

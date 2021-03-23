from odoo import fields, models


class StockLocation(models.Model):
    _name = "stock.location.ept"
    _description = "To store the stock location details"

    name = fields.Char(string="Stock Location Name", help="Enter stock location name",
                       required=True)
    parent_id = fields.Many2one(string="Parent", help="Parent id of stock location",
                                comodel_name="stock.location.ept")
    location_type = fields.Selection(selection=[
        ('Vendor', 'Vendor'),
        ('Customer', 'Customer'),
        ('Internal', 'Internal'),
        ('Inventory Loss', 'Inventory Loss'),
        ('Production', 'Production'),
        ('Transit', 'Transit'),
        ('View', 'View')
    ], string="Location Type", help="Select location type")
    is_scrap_location = fields.Boolean(string="Scrap Location", help="Is scrap location")

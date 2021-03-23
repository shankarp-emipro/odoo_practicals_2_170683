from odoo import fields, models


class ResCityEpt(models.Model):
    _name = "res.city.ept2"
    _description = "To store city data"

    name = fields.Char(string="City Name", help="Enter city name")
    state_id = fields.Many2one(string="State Id", help="Select state id", comodel_name="res.state.ept2")
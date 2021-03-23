from odoo import fields, models


class ResPartner(models.Model):
    _name = "res.partner.ept4"
    _description = "To store res partner data"

    name = fields.Char(string="Res Partner Name", help="Enter res partner name")
    street1 = fields.Char(string="Street-1", help="Enter street1")
    street2 = fields.Char(string="Street-2", help="Enter street2")
    country_id = fields.Many2one(string="Country", help="Country id",
                                 comodel_name="res.country.ept2")
    state_id = fields.Many2one(string="State", help="State id", comodel_name="res.state.ept2")
    city_id = fields.Many2one(string="City", help="City id", comodel_name="res.city.ept2")
    zip_code = fields.Char(string="ZipCode", help="Enter zip code")
    email = fields.Char(string="Email", help="Enter email")
    mobile = fields.Char(string="Mobile", help="Enter mobile number")
    phone = fields.Char(string="Phone", help="Enter phone number")
    photo = fields.Image(string="Image", help="Select photo")
    website = fields.Char(string="Website", help="Enter website")
    active = fields.Boolean(string="Active", help="Mark active", default=True)
    parent_id = fields.Many2one(string="Parent", help="Parent id",
                                comodel_name="res.partner.ept4",
                                ondelete="cascade")
    child_ids = fields.One2many(string="Child", help="Child ids",
                                comodel_name="res.partner.ept4",
                                inverse_name="parent_id")
    address_type = fields.Selection(selection=[
        ('Invoice', 'Invoice'),
        ('Shipping', 'Shipping'),
        ('Contact', 'Contact')
    ], string="AddressType", help="Select address type")

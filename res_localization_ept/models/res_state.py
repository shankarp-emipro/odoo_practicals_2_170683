from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResStateEpt(models.Model):
    _name = "res.state.ept2"
    _description = "To store states"

    name = fields.Char(string="State", help="Enter state")
    state_code = fields.Char(string="State code", help="Enter state code")
    country_id = fields.Many2one(comodel_name="res.country.ept2", string="Country Id", help="Select country id")
    city_ids = fields.One2many(string="Cities", comodel_name="res.city.ept2", inverse_name="state_id")

    @api.constrains('state_code')
    def validate_state_code(self):
        record = self.search([('state_code', 'ilike', self.state_code), ('id', '!=', self.id)])
        if record:
            raise ValidationError(_("State code already exists."))

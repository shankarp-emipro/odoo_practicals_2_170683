from odoo import fields, models


class RelatedEmployeeAddress(models.Model):
    _name = "related.employee.address"

    name = fields.Char(string="Name", help="Contact name")
    contact_number = fields.Char(string="Number", help="Contact number")
    street1 = fields.Char(string="Street1", help="Street1")
    street2 = fields.Char(string="Street2", help="Street2")
    city = fields.Char(string="City", help="City")
    contact_relation_id = fields.Many2one(string="Contact Relation", help="Contact relation id",
                                          comodel_name="employee.contact.relation")
    contact_relation_occupation_id = fields.Many2one(string="Contact Occupation",
                                                     help="Contact relation occupation id",
                                                     comodel_name="employee.contact.occupation")

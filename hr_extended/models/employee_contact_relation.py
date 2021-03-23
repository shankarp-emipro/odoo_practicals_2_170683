from odoo import fields, models


class EmployeeContactRelation(models.Model):
    _name = "employee.contact.relation"
    _description = "To store the employee contact relation data."

    name = fields.Char(string="Relation", help="Employee relation")

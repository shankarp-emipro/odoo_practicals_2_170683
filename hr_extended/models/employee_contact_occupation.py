from odoo import fields, models


class EmployeeContactOccupation(models.Model):
    _name = "employee.contact.occupation"
    _description = "To store the employee contact occupation data."

    name = fields.Char(string="Occupation", help="Employee occupation")

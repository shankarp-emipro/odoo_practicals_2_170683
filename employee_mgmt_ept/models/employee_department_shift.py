from odoo import fields, models, api


class EmployeeDepartmentShift(models.Model):
    _name = "employee.department.shift.ept"
    _description = "To store employee department shift"
    _rec_name = 'shift'     # to recognize shift as name

    shift = fields.Selection(selection=[
        ('Morning','Morning'),
        ('Afternoon','Afternoon'),
        ('Evening','Evening'),
        ('Night','Night')
    ], string="Shift", help="Select shift")
    
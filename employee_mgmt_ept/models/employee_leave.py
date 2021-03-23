from odoo import fields, models, api


class EmployeeLeave(models.Model):
    _name = "employee.leave"
    _description = "To store employee leave data"
    _rec_name = 'employee_id'   # to recognize employee_id as name

    employee_id = fields.Many2one(string="Employee Id", help="Employee id", comodel_name="employee.ept2")
    department_id = fields.Many2one(string="Department Id", help="Department id", comodel_name="employee.department.ept")
    start_date = fields.Date(string="Start date", help="Enter start date")
    end_date = fields.Date(string="End date", help="Enter end date")
    status = fields.Selection(selection=[
        ('Draft','Draft'),
        ('Approved','Approved'),
        ('Refused','Refused'),
        ('Cancelled','Cancelled')
    ], string="Status", help="Select status")
    leave_description = fields.Char(string="Leave description", help="Enter leave description")
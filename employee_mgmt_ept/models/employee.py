from odoo import fields, models, api


class Employee(models.Model):
    _name = "employee.ept2"
    _description = "To store employee data"

    name = fields.Char(string="Employee Name", help="Enter employee name", required=True)
    department_id = fields.Many2one(string="Department Name of Employee", help="Department Name of Employee", comodel_name="employee.department.ept")
    shift_id = fields.Many2one(string="Shift Id", help="Shift Id", comodel_name="employee.department.shift.ept")
    job_position = fields.Char(string="Job Position", help="Enter job position")
    salary = fields.Float(string="Salary", help="Enter salary", digits=(6,2))
    hire_date = fields.Date(string="Hire Date", help="Enter hire date")
    gender = fields.Selection(selection=[
        ('Male','Male'),
        ('Female','Female'),
        ('Transgender','Transgender')
    ], string="Gender", help="Select gender")
    job_type = fields.Selection(selection=[
        ('Permanent', 'Permanent'),
        ('Ad Hoc', 'Ad Hoc'),
    ], string="Job Type", help="Select job type")
    is_manager = fields.Boolean(string="Is Manager", help="Is manager")
    manager_id = fields.Many2one(string="Manager Id", help="Manager id", comodel_name="employee.ept2")
    related_user_id = fields.Many2one(string="Related User", help="Related user", comodel_name="res.users")
    employee_ids = fields.One2many(string="Employee Ids", help="Employee ids", comodel_name="employee.ept2", inverse_name="manager_id")
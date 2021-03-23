from odoo import fields, models, api


class EmployeeDepartment(models.Model):
    _name = "employee.department.ept"
    _description = "To store the employee department data"

    name = fields.Char(string="Department Name", help="Enter department name", required=True)
    employee_ids = fields.One2many(string="Employee Ids", help="Employee Ids", comodel_name="employee.ept2", inverse_name="department_id")
    department_manager_id = fields.Many2one(string="Manager Ids", help="Manager Ids", comodel_name="res.users")
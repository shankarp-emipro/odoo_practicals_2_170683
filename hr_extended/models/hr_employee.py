from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    joining_date = fields.Date(string="Joining Date", help="Joining date of employee")
    leaving_date = fields.Date(string="Leaving Date", help="Leaving date of employee")
    pf_applicable = fields.Boolean(string="PF Applicable", help="Mark if pf is applicable")
    pf_number = fields.Char(string="PF Number", help="PF number of employee")
    related_contact_id = fields.Many2one(string="Related Contact", help="Related contact id",
                                         comodel_name="related.employee.address")
    tag_ids = fields.One2many(string="Tags", help="Tag ids", comodel_name="project.tags",
                              compute="_compute_create_employee_skill_line")

    def _compute_create_employee_skill_line(self):
        """
        This method fetches the tags that are associated with the user and sets it in tag_ids field which helps
        displaying tag lines.
        :return: -
        """
        tag_ids = self.env['project.task'].search([('user_id', '=', self.user_id.id), ('tag_ids.id', '!=', False)]).tag_ids.ids
        self.tag_ids = tag_ids if tag_ids else False

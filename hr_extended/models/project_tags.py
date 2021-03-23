from odoo import fields, models


class ProjectTags(models.Model):
    _inherit = "project.tags"

    user_ids = fields.Many2many(string="Users", help="User ids", comodel_name="res.users",
                                compute="_compute_fetch_users_of_tag")
    hr_employee_id = fields.Many2one(string="Employee", help="HR employee id",
                                     comodel_name="hr.employee")
    tag_id = fields.Many2one(string="Tag", help="Tag name of the project",
                             comodel_name="project.tags")
    tag_frequency = fields.Integer(string="Frequency", help="Tag Frequency (count of the tag)",
                                   compute="_compute_tag_frequency")

    def _compute_tag_frequency(self):
        """
        To get the frequency count of the tasks against the tag for the user of the employee
        :return: -
        """
        for tag_id in self:
            tag_id.tag_frequency = self.env['project.task'].search_count(
                [('user_id', '=', self._context.get('usr_id')), ('tag_ids', 'in', tag_id.id)])

    def _compute_fetch_users_of_tag(self):
        """
        To fetch those users which are associated with particular tag
        :return: -
        """
        for tag in self:
            tag.user_ids = list(set(map(lambda task: task.user_id.id,
                                        self.env['project.task'].search(
                                            [('tag_ids', 'in', tag.id)]))))

    def view_tasks(self):
        """
        To view the task list associated with the tags
        :return: -
        """
        action = {
            'name': 'My Tasks',
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('user_id', '=', self._context['usr_id']), ('tag_ids', 'in', self.id)]
        }
        return action

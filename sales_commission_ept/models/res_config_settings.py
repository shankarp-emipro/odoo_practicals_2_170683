from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    commission_based_on = fields.Selection(selection=[
        ('confirm_sales_orders', 'Confirm sales orders'),
        ('confirm_invoice', 'Confirm invoice'),
        ('paid_invoice', 'Paid invoice')
    ], string="Commission BasedOn", help="Commission based on")
    manager_commission_calculation = fields.Selection(selection=[
        ('based_on_individual_sales', 'Based on individual sales'),
        ('based_on_total_sales_of_team_members', 'Based on Total sales of team members')
    ], string="Sales manager commission calculation", help="Sales manager commission calculation")
    individual_commission_percentage = fields.Float(string="Commission Percentage",
                                                    help="Commission percentage",
                                                    digits=(6, 2))
    total_commission_percentage = fields.Float(
        string="Commission percentage on sales team's total amount",
        help="Commission percentage on sales team's total amount",
        digits=(6, 2))
    commission_product_id = fields.Many2one(string="Commission product", help="Commission product",
                                            comodel_name="product.product")

    def default_get(self, fields):
        """
        Fetches the value from the ir.config_parameter model and sets in the field
        :param fields: fields of the res.config.settings model
        :return: - dictionary of fields along with its value
        """
        defaults = super(ResConfigSettings, self).default_get(fields)
        defaults['commission_based_on'] = self.env[
            'ir.config_parameter'].sudo().get_param(
                'sales_commission_ept.commission_based_on')

        defaults['manager_commission_calculation'] = self.env[
            'ir.config_parameter'].sudo().get_param(
                'sales_commission_ept.manager_commission_calculation')

        defaults['individual_commission_percentage'] = self.env[
            'ir.config_parameter'].sudo().get_param(
                'sales_commission_ept.individual_commission_percentage')

        defaults['total_commission_percentage'] = self.env[
            'ir.config_parameter'].sudo().get_param(
                'sales_commission_ept.total_commission_percentage')

        defaults['commission_product_id'] = int(self.env[
            'ir.config_parameter'].sudo().get_param(
                'sales_commission_ept.commission_product_id'))
        return defaults

    def set_values(self):
        """
        To set the current selected value in the ir.config_parameter model
        :return: -
        """
        val = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sales_commission_ept.commission_based_on',
                                                         self.commission_based_on)

        self.env['ir.config_parameter'].sudo().set_param(
            'sales_commission_ept.manager_commission_calculation',
            self.manager_commission_calculation)

        self.env['ir.config_parameter'].set_param(
            'sales_commission_ept.individual_commission_percentage',
            self.individual_commission_percentage)

        self.env['ir.config_parameter'].set_param(
            'sales_commission_ept.total_commission_percentage',
            self.total_commission_percentage)

        self.env['ir.config_parameter'].set_param(
            'sales_commission_ept.commission_product_id',
            self.commission_product_id.id)

        return val

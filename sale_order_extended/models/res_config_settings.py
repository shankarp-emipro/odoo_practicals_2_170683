from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    company_id_ept = fields.Many2one(string="Company", help="Company id",
                                     comodel_name="res.company")
    config_shipping_id = fields.Many2one(string="Config Shipping", help="Config shipping id",
                                         comodel_name="product.product")
    product_id = fields.Many2one(string="Product Default",
                                 help="Default product used for payment advances",
                                 domain="[('type', '=', 'service')]",
                                 comodel_name="product.product",
                                 config_parameter='sale.default_product_id')
    default_days = fields.Selection(selection=[
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday')
    ], string="Days", help="Days of the week", default_model="res.company")
    group_is_salesperson_group = fields.Boolean(string="Salesperson Group",
                                                help="Salesperson group",
                                                implied_group="sale_order_extended.group_sale_order_extended_salesperson")
    module_test_ept = fields.Boolean(string="Test Ept", help="Test ept module install")

    partner_ept_id = fields.Many2one(string="Partner", help="Partner id",
                                     comodel_name="res.partner",
                                     related="company_id_ept.partner_ept_id", readonly=False)

    def execute(self):
        super(ResConfigSettings, self).execute()
        self.company_id_ept.write({
            'shipping_id': self.config_shipping_id.id
        })

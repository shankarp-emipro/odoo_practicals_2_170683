from odoo import fields, models


class CrmLeadLine(models.Model):
    _name = "crm.lead.line.ept"
    _description = "To store crm lead line data"

    product_id = fields.Many2one(string="Product", help="Product id", comodel_name="product.ept4")
    expected_sell_qty = fields.Float(string="Expected sell qty", help="Enter expected sell qty",
                                     digits=(6, 2))
    uom_id = fields.Many2one(string="UOM", help="Enter uom id", comodel_name="product.uom.ept4")
    lead_id = fields.Many2one(string="Lead", help="Lead id", comodel_name="crm.lead.ept2")

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    parent_line_id = fields.Many2one(string="Parent", help="Parent line id",
                                     comodel_name="sale.order.line")
    child_ids = fields.One2many(string="Child", help="Child ids", comodel_name="sale.order.line",
                                inverse_name="parent_line_id")
    profit_margin = fields.Float(string="Profit margin",
                                 help="Profit margin - percentage of the profit", digits=(6, 2),
                                 compute="_compute_profit_value_margin")
    profit_value = fields.Float(string="Profit value",
                                help="Profit value (cost_price - unit_price)", digits=(6, 2),
                                compute="_compute_profit_value_margin")
    cost_price = fields.Float(string="Cost price", help="Cost price (standard price)",
                              digits=(6, 2), compute="_compute_get_cost_price", store=True)
    tax_id = fields.Many2one(string="Tax", help="Tax", comodel_name="account.tax")

    @api.depends('product_id')
    def _compute_get_cost_price(self):
        # To store the cost price of the product when the product is changed
        # The reason to store this is when the product's cost price is changed in future at that
        # time the value of the line should not be changed unless the product is changed.
        # returns -
        for line in self:
            line.cost_price = line.product_id.standard_price

    def _compute_profit_value_margin(self):
        # To calculate the profit value and the profit margin of the sale order line.
        # returns -
        for line in self:
            profit_value = (line.price_unit - line.cost_price)
            line.profit_value = profit_value * line.product_uom_qty
            if line.cost_price > 0:
                line.profit_margin = (profit_value / line.cost_price) * 100
            else:
                line.profit_margin = 0.0

from odoo import models


class StockPickingReport(models.AbstractModel):
    _name = "report.sale_ept.report_stock_picking_ept"

    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name(
            'sale_ept.report_stock_picking_ept')
        pickings = self.env[report.model].browse(docids)
        stock_moves = {}
        for picking in pickings:
            for move_line in picking.stock_move_ids:
                if stock_moves.get(move_line.product_id.name):
                    stock_moves[move_line.product_id.name].append({
                        'source_location_id': move_line.source_location_id.name if move_line.source_location_id.name else '-',
                        'qty_to_deliver': move_line.qty_to_deliver
                    })
                else:
                    stock_moves.update({
                        move_line.product_id.name: [{
                            'source_location_id': move_line.source_location_id.name if move_line.source_location_id.name else '-',
                            'qty_to_deliver': move_line.qty_to_deliver
                        }]
                    })

        return {
            'stock_moves': stock_moves
        }

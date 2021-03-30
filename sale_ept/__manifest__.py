{
    'name': 'Sale EPT',
    'version': '14.0.0.1',
    'category': '',
    'description': """
        This module is used to store the data of sale.
    """,
    'author': 'Emipro Technologies (P) Ltd.',
    'depends': [
        'base',
        'res_localization_ept',
        'mail'
    ],
    'data': [
        'security/employee_security.xml',
        'security/ir.model.access.csv',
        'views/view_product_category.xml',
        'views/view_product_uom_category.xml',
        'views/view_product_uom.xml',
        'views/view_product.xml',
        'views/view_res_partner.xml',
        'views/view_sale_order.xml',
        'views/view_crm_lead.xml',
        'views/view_crm_team.xml',
        'views/view_stock_location.xml',
        'views/view_stock_warehouse.xml',
        'views/view_stock_move.xml',
        'views/view_stock_picking.xml',
        'views/view_stock_inventory.xml',
        'wizard/wizard_product_stock_update.xml',
        'views/view_account_tax.xml',
        'report/sale_order_report_templates.xml',
        'report/sale_order_report.xml',
        'views/sale_ept_menu.xml',
        'data/ir_sequence_data.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False
}

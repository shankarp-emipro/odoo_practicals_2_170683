{
    'name': 'Sales Commission Ept',
    'version': '1.0.1',
    'category': 'Sales/Commission',
    'author': 'Emipro Technologies (P) Ltd.',
    'summary': 'Sales commission',
    'description': """
        This module contains all the sales commission related calculations.
        Sale order is also inherited and its tax_id field which is Many2many is
        converted Many2one.
    """,
    'depends': ['sale'],
    'data': [
        'security/sales_commission_ept_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/sale_order_extended_view.xml',
        'views/sales_commission_ept_views.xml',
        'views/sales_commission_line_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/reset_draft_message.xml',
        'views/sales_commission_ept_menus.xml'

    ],
    'installable': True,
    'auto_install': False
}

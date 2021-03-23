{
    'name': 'Sale Order Extended',
    'version': '1.0.1',
    'category': 'sales',
    'description': """
        This module extends the sale module.
    """,
    'summary': """
        In this module crm.lead model's many2one field is taken in sale.order model. When new quotation is created then
        there is a field named tag_ids which should set the default value 'From Lead'
    """,
    'author': 'Emipro Technologies (P) Ltd.',
    'depends': ['sale_crm'],
    'data': [
        'security/employee_security.xml',
        'security/ir.model.access.csv',
        'data/data_crm_tag.xml',
        'views/sale_order.xml',
        'views/product_template_view.xml',
        'views/res_company_view.xml',
        'wizard/wizard_sales_info_update.xml',
        'views/res_config_settings_view.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False
}

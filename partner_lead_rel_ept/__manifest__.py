{
    'name': 'Partner Lead',
    'version': '1.0.0',
    'category': '',
    'description': """
        This module is used to store partner lead rel data.
    """,
    'author': 'Shankar Pariyar',
    'depends': ['crm'],
    'data': [
        'security/employee_security.xml',
        'security/ir.model.access.csv',
        'views/partner_lead_rel.xml',
        'views/menu_partner_lead_rel_ept.xml',
        'data/ir_sequence_data.xml'
    ],
    'installable': True,
    'auto_install': False
}

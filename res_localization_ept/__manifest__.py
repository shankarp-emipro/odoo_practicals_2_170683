{
    'name': 'Res Localization Ept',
    'version': '1.0.0',
    'category': '',
    'description': """
        This module is used to store the details of res localization.
    """,
    'author': 'Shankar Pariyar',
    'depends': ['base'],
    'data': [
        'security/localization_security.xml',
        'security/ir.model.access.csv',
        'views/view_res_country.xml',
        'views/view_res_state.xml',
        'views/view_res_city.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False
}

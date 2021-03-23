{
    'name': 'HR Extended',
    'version': '1.0.1',
    'category': 'Human Resources/Employees',
    'description': """
        This module extends the hr module.
    """,
    'summary': 'To add extra fields in hr.employee model and to add some elements in view',
    'author': 'Emipro Technologies (P) Ltd.',
    'depends': ['project','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/related_employee_address.xml',
        'views/employee_contact_relation_view.xml',
        'views/employee_contact_occupation_view.xml',
        'views/hr_employee_extended_view.xml',
        'views/project_tags_extended_view.xml',
        'views/hr_extended_menu.xml',
    ],
    'installable': True,
    'auto_install': False
}

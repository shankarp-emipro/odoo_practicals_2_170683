{
    'name': 'Employee Management Ept',
    'version': '1.0.0',
    'category': '',
    'description': """
        This module is used to manage employee.
    """,
    'author': 'Shankar Pariyar',
    'depends': ['base'],
    'data': [
        'security/employee_security.xml',
        'security/ir.model.access.csv',
        'views/view_department.xml',
        'views/view_shift.xml',
        'views/view_employee.xml',
        'views/view_leave.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False
}

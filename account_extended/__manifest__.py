{
    'name': 'Account Extended',
    'version': '1.0.1',
    'category': 'invoice/account',
    'description': """
        This module extends the account module.
    """,
    'summary': 'To add wizard in partner screen to validate the invoices.',
    'author': 'Emipro Technologies (P) Ltd.',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron_invoice_validate.xml',
        'views/res_partner_view.xml',
        'wizard/partner_invoices_wizard.xml'
    ],
    'installable': True,
    'auto_install': False
}

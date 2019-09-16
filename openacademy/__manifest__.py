{
    'name': "Openacademy",
    'version': '1.0',
    #'depends': ['base'],
    'depends': ['base', 'board','website','website_sale'],
    #'depends': ['website'],
    #'depends': ['website_sale'],
    'author': "Ipsita",
    'category': 'Category',
    'description': """
    Courses for student
    """,
    # data files always loaded at installation
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/courses_view.xml',
        'views/partner.xml',
        'report/reports.xml',
        'views/session_board.xml',
        'views/views.xml',
        'views/template.xml',
        'views/data.xml',
        'views/assets.xml',
    ],
    'qweb':['static/src/xml/template.xml'],
    'demo': [
        'views/demo.xml',
    ],
}

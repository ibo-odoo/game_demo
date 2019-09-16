{
    'name': "BusDemo",
    'version': '1.0',
    'depends': ['base','bus'],
    'author': "Ipsita",
    'category': 'Category',
    'description': """
    For student
    """,
    # data files always loaded at installation
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/app_view.xml',
        'views/assets.xml',
    ],
    'qweb':['static/src/xml/bus_widget.xml'],
}

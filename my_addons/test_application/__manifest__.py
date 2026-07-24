{
    'name':'Test Application',
    'version':'1.0',
    'summary':"我的测试模块",
    'description':"测试模块的详细描述",
    'author':'silvertune',
    'category':'',
    'depends':['base','product','account','mail'],
    'data':[
        'security/ir.model.access.csv',
        'views/l_sale_order_views.xml',
        'views/menu_views.xml',
        'views/res_partner_notebook_view.xml',
        'wizard/l_sale_order_wizard.xml',
    ],
    'installable':True,
    'application':True,
    'license': 'LGPL-3',

}
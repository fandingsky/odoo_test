from odoo import api, fields, models

class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit =['product.template','l.test.abstract']


    l_barcode = fields.Char(string="我的条形码")
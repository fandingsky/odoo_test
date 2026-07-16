from odoo import api,models,fields


class LSaleOrderLine(models.Model):
    _name = "l.sale.order.line"
    _description = "销售订单行"
    _order = "product_id desc "

    name = fields.Char(string="明细行")
    # 这里product是product模型里的一个字段，product.product是模型的名字
    # 因此需要在manifest文件里去依赖product模块
    product_id = fields.Many2one('product.product', string="产品", help="这是我的产品")
    order_id = fields.Many2one('l.sale.order', string="订单", help="这是我的订单")

    # flout类型的字段，dights是小数点后几位,Product Unit是产品单价单位的意思，在odoo的设置里调整
    # price_unit = fields.Float(string="单价", help="这是我的单价", digits=2)在19.0版本中已经不支持了，必须使用digits='Product Unit'，否则会报错
    # price_unit = fields.Float(string="单价", help="这是我的单价", digits=(16,2)),digits=(最大值,小数点后的值)
    price_unit = fields.Float(string="单价", help="这是我的单价",digits='Product Unit')
    amount_total = fields.Float(string="总价", digits=(16,2))
    qty = fields.Float(string="数量", digits='Product Unit')

    # 这里第二个因素是relation，第三个因素是column1，第四个因素是column2，第五个因素是string
    # column1是当前模型的字段，column2是关联模型的字段，这里是可以自定义的
    # 也是可以不写的，写了就会在数据库里生成一个表，表名是relation，字段是column1和column2
    tax_ids = fields.Many2many('account.tax', 'l_sale_order_line_account_tax_rel',
                               'l_sale_order_line','account_tax_id'
                               ,string="税项")

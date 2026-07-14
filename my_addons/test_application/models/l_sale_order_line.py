from odoo import api,models,fields


class LSaleOrderLine(models.Model):
    _name = "l.sale.order.line"
    _description = "销售订单行"
    _order = "id desc"

    name = fields.Char(string="明细行")
    # 这里product是product模型里的一个字段，product.product是模型的名字
    # 因此需要在manifest文件里去依赖product模块
    product_id = fields.Many2one('product.product', string="产品", help="这是我的产品")
    order_id = fields.Many2one('l.sale.order', string="订单", help="这是我的订单")
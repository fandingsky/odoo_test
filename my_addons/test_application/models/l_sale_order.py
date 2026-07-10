from odoo import api,models,fields

class LSaleOrder(models.Model):
    _name ="l.sale.order"
    _description = "销售订单"

    name =fields.Char(string="订单编号",help="这是我的订单编号"
                        # ,readonly=1
                      )
    note = fields.Text(string="备注", help="这是我的备注"
                        # ,required=1
                       ,copy=False )
    sequence = fields.Integer(string="整数",help="这是我的整数")
    qty = fields.Float(string="浮点",help="浮点")
    is_bool = fields.Boolean(string="布尔",help="布尔类型")

    state = fields.Selection([('draft','草稿'),
                              ('confirm','已确认'),
                              ('paid','已支付')],
                             string="状态",
                             help="这是我的状态",
                             default='draft')
    date_01 = fields.Date(string="日期",help="这是我的日期",
                          default=fields.Date.today())
    date_02 = fields.Datetime(string="日期时间",help="这是我的日期时间",
                              default=fields.Datetime.now())
    image =fields.Image(string="图片",help="这是我的图片")
    binary = fields.Binary(string="二进制",help="这是我的二进制")
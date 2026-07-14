from odoo import api,models,fields

class LSaleOrder(models.Model):
    _name ="l.sale.order"
    _description = "销售订单"
    # _order是排序功能，以name为基准
    _order = "id desc"

    def _compute_name(self):
        print('_compute_name',self)
        for record in self:
            if record.state and record.id:
                record.name = f"{record.state}/{record.id}"
            else:
                record.name = "未确认"

    name =fields.Char(string="订单编号",help="这是我的订单编号"
                    ,compute="_compute_name"
                    # ,store=True
                      )
    validate_date = fields.Datetime(string="有效期",help="这是我的确认时间",default=fields.Date.today())
    payment_type = fields.Selection([('v_1','立即付款'),('v_2','7天'),('v_3','15天'),('v_4','30天')],string="付款方式",help="这是我的付款方式",default='v_1')
    partner_id=fields.Many2one('res.partner',string="客户",help="这是我的客户")
    line_ids = fields.One2many('l.sale.order.line','order_id',string="订单明细",help="这是我的订单明细")
    # many2one和one2many是相互关联的，one2many是many2one的反向关系
    # 必须对应
    note = fields.Html(string="备注",help="这是我的备注")
    state =fields.Selection([('draft','草稿'),('confirm','已确认'),('done','已完成')],string="状态",help="这是我的状态",default='draft')

    # 加了api.depends装饰器后，只有当note字段发生变化时，
    # 触发_compute_name方法的执行，从而提高了性能。
    # @api.depends('note')
    # def _compute_name(self):
    #     print(self)
    #     for record in self:
    #         if record.note:
    #             record.name = f"{record.note}/{record.id}"
    #         else:
    #             record.name = "未确认"

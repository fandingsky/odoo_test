from odoo import api,models,fields
from odoo.exceptions import ValidationError


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
                    ,store=True
                    ,readonly=False
                      )
    validate_date = fields.Datetime(string="有效期",help="这是我的确认时间",default=fields.Date.today())
    payment_type = fields.Selection([('v_1','立即付款'),('v_2','7天'),('v_3','15天'),('v_4','30天')],string="付款方式",help="这是我的付款方式",default='v_1')
    partner_id=fields.Many2one('res.partner',string="客户",help="这是我的客户")
    line_ids = fields.One2many('l.sale.order.line','order_id',string="订单明细",help="这是我的订单明细")
    # many2one和one2many是相互关联的，one2many是many2one的反向关系
    # 必须对应
    note = fields.Html(string="备注",help="这是我的备注")
    state =fields.Selection([('draft','草稿'),('confirm','已确认'),('done','已完成')],string="状态",help="这是我的状态",default='draft')
    barcode = fields.Char(string="订单条码")

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

    @api.constrains('barcode')
    def constraint_barcode(self):
        for record in self:
            domain = [('barcode', '=', record.barcode), ('id', '!=', record.id)]
            if self.search(domain, limit=1):
                raise ValidationError('订单条码不能重复')



    # 回到上一页的办法，不知为何act_window_close无法使用
    # 下面这个强制定向方法也无法使用
    # return {
    #     'type': 'ir.actions.act_window',
    #     'name': '订单列表',
    #     'res_model': 'l.sale.order',
    #     'view_mode': 'list',
    #     'target': 'main',
    # }
    def go_back(self):
        # 这里env是环境变量，env.context是环境变量的上下文，env.context.get()是获取上下文变量的值
        previous_action = self.env.context.get('previous_action_id')
        if previous_action:
            # 这里是通过xml_id获取动作，fore_xml_id是获取xml_id对应的动作
            return self.env['ir.actions.act_window']._for_xml_id(previous_action)
        else:
            # 这里是默认的跳转，跳转到订单列表
            return self.env['ir.actions.act_window']._for_xml_id('test_application.l_sale_order_act_window')


    # 通过按钮对state进行修改
    def state_to_confirm(self):
        self.write({'state':'confirm'})

    def state_to_draft(self):
        self.write({'state': 'draft'})

    def state_to_done(self):
        self.write({'state': 'done'})

    def delete_order(self):
        # 先删除关联的订单行（因为 ondelete='restrict' 会阻止级联删除）
        self.line_ids.unlink()
        # 再删除当前订单
        self.unlink()
        # 返回订单列表视图，避免留在已删除的页面
        return self.go_back()


from odoo import models,fields,api
from ..models import l_test_abstract


class LSaleOrderWizard(models.TransientModel):
    _name = "l.sale.order.wizard"
    _inherit = "l.test.abstract"

    name = fields.Char(string="我是第一个向导")
    order_id = fields.Many2one('l.sale.order',string="订单")

    def action_confirm(self):
        print("向导输入的name是：", self.name)
        self.ensure_one()
        print("关联订单 ID：", self.order_id.id if self.order_id else "无")
        if self.order_id:
            self.order_id.note = self.name
            print("已将备注写入订单", self.order_id.name)
        return {'type': 'ir.actions.act_window_close'}
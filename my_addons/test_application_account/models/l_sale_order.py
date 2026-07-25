from odoo import api,models,fields,Command
from odoo.exceptions import ValidationError


class LSaleOrder(models.Model):
    _inherit = "l.sale.order"



    def state_to_done(self):
        res = super().state_to_done()
        for order in self:
            if not order.partner_id:
                raise ValidationError("无法创建发票：订单 %s 没有指定客户" % order.name)
            line_commands=[]
            for line in order.line_ids:
                if line.price_unit * line.qty <=0:
                    continue
                line_commands.append(Command.create({
                    'name':line.product_id.display_name or line.name or '订单行',
                    'quantity':line.qty,
                    'price_unit':line.price_unit,
                }))

            if not line_commands:
                line_commands.append(Command.create({
                    'name':'订单行',
                    'quantity':1,
                    'price_unit':0,
                }))

            invoice_vals = {
                'partner_id':order.partner_id.id,
                'move_type':'out_invoice',
                'invoice_line_ids':line_commands,
            }
            invoice = self.env['account.move'].create(invoice_vals)
        return res
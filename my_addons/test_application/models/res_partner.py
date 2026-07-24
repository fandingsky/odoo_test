from odoo import api,fields,models

class ResPartner(models.Model):

    _inherit = 'res.partner'
    l_sale_order_ids = fields.One2many('l.sale.order', 'partner_id', string="销售订单")
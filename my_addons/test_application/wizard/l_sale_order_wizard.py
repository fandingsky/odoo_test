from odoo import models,fields,api
from ..models import l_test_abstract


class LSaleOrderWizard(models.TransientModel):
    _name = "l.sale.order.wizard"
    _inherit = "l.test.abstract"

    name = fields.Char(string="我是第一个向导")
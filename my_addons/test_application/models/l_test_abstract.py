from odoo import api,models,fields


class LTestAbstract(models.AbstractModel):
    _name = "l.test.abstract"

    approve_state = fields.Selection([('done','agree'),('waiting','等待审批'),('refuse','拒绝')]
                                     ,string="状态",default='waiting')

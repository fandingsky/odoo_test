from odoo import api,models,fields


class LSaleOrderLine(models.Model):
    _name = "l.sale.order.line"
    _description = "销售订单行"
    _order = "product_id desc "

    name = fields.Char(string="明细行")
    # 这里product是product模型里的一个字段，product.product是模型的名字
    # 因此需要在manifest文件里去依赖product模块
    product_id = fields.Many2one('product.product', string="产品", help="这是我的产品")
    order_id = fields.Many2one('l.sale.order', string="订单", help="这是我的订单",
    # 这里ondelete="cascade"表示如果删除了订单，那么订单行也会被删除，这就是级联操作
    # 如果是ondelete="restrict"的话，如果有外键就无法删除，如果没有就可以删除
                               ondelete="restrict"
                               )

    # flout类型的字段，dights是小数点后几位,Product Unit是产品单价单位的意思，在odoo的设置里调整
    # price_unit = fields.Float(string="单价", help="这是我的单价", digits=2)在19.0版本中已经不支持了，必须使用digits='Product Unit'，否则会报错
    # price_unit = fields.Float(string="单价", help="这是我的单价", digits=(16,2)),digits=(最大值,小数点后的值)
    price_unit = fields.Float(string="单价", help="这是我的单价",digits='Product Unit')
    amount_total = fields.Float(string="总价", digits=(16,2),compute="compute_total",store="True")
    qty = fields.Float(string="数量", digits='Product Unit')

    # 这里第二个因素是relation，第三个因素是column1，第四个因素是column2，第五个因素是string
    # column1是当前模型的字段，column2是关联模型的字段，这里是可以自定义的
    # 也是可以不写的，写了就会在数据库里生成一个表，表名是relation，字段是column1和column2
    tax_ids = fields.Many2many('account.tax', 'l_sale_order_line_account_tax_rel',
                               'l_sale_order_line','account_tax_id'
                               ,string="税项")

    def button_add(self):
        """
        来操作tax_ids字段，添加一个字段
        (0,0,{'name':'21%','amount':21.0})表示添加一个新的记录
        (1,tax.id,{'name':'21%','amount':21.0})表示更新已有的记录
        (2,tax.id,0)表示删除已有的记录,这里0为占位符号
        (4,tax.id)表示关联已有的记录
        (3,tax.id)表示解除关联已有的记录
        (5,)表示删除所有关联的记录
        """
        print(self.tax_ids)
        self.tax_ids = [(0,0,{'name':'21%','amount':21.0})]

        # 一次性添加多个字段的写法，适用于下面的其他方法
        # self.tax_ids = [(0,0,{'name':'21%','amount':21.0}),(0,0,{'name':'4%','amount':4.0})]

    def button_link(self):
        """
        来操作tax_ids字段,添加关联的已有字段
        """
        print(self.tax_ids)
        self.tax_ids = [(4,6,0),(4,1,0)]

        # 因为在表中tax_ids并没有关联到这个所以并不能用下面的方式写
        # for tax in self.tax_ids:
        #     if tax.name == '21%':
        #         self.tax_ids = [(4,tax.id,0)]


    def button_update(self):
        """
        来操作tax_ids字段,更新已有字段
        """
        print(self.tax_ids)

        for tax in self.tax_ids:
            if tax.name == '4%':
                self.tax_ids = [(1,tax.id, {'name': '21%', 'amount': 21.0})]

    def button_updateall(self):
        """
        来操作tax_ids字段,更新所有已有字段
        本质上是把一个删除全部关联功能和一个添加关联功能放在一起操作
        self.tax_ids[(6,0,[id1,id2])]
        id1和id2是税率的对应id
        一般来说这个使用的场所最多
        """
        print(self.tax_ids)
        self.tax_ids = [(6,0,[1,3,6])]


    def button_delete(self):
        """
        删除，但是是所有数据库里的都删除了，所以很少用这种
        基本上都是用(3,id,0)的从关系中一处
        """
        print(self.tax_ids)

        for tax in self.tax_ids:
            if tax.name == '21%':
                self.tax_ids = [(2,tax.id,0)]

    def button_unlink(self):
        """
        来操作tax_ids字段,删除关联的已有字段
        """
        print(self.tax_ids)

        for tax in self.tax_ids:
            if tax.name == '21%':
                self.tax_ids = [(3,tax.id,0)]


    def button_unlinkall(self):
        """
        来操作tax_ids字段,清空所有关联的已有字段
        """
        print(self.tax_ids)
        self.tax_ids = [(5,0,0)]

#         如果把Command添加进来也可以写为
#         self.tax_ids = [Command.clear]

    @api.depends('price_unit','qty')
    def compute_total(self):
        self.amount_total=self.price_unit * self.qty
# 模型的继承：

    models.TransientModel(临时/向导模型)
        1.自动存储数据但是有生命周期
        2.向导模型临时存储处理数据，数据并不会持久化存储
        3.创建临时表-临时存储-定期清理-可被继承-可以实例化-适用于临时操作/向导      
        4.可以用来做柱状图、饼状图、折线图
        5.向导模型需要定义权限


    models.AbstractModel(抽象模型)
        1.抽象模型不存储数据，只作为模
        2.不创建表-不存储数据-只能被继承-不能实例化-适用于代码复用、公共逻辑
        3.抽象类不需要定义权限

继承的样式：

    1.经典继承，类继承
    class InheritedModel(models.Model):
        _inherit = 'parent.model'

        # 字段定义
        new_field = fields.Char(string='New Field')

        #方法重写
        def existing_method(self):
            调用父辈方法
            super(InheritedModel, self).existing_method()  
            # 新方法逻辑
            return result

    2.扩展继承(混合继承)
    class ExtendeModel(models.Model):
        _name = 'new.model'
        _inherit=['model1','model2','model3']

        #继承多个模型的特性

        new_field = fields.Char(string='Combined Field')

# 模型的约束与数据校验
1.模型约束：
    _sql_constraints = [
        ('unique_barcode', #约束名称
        'unique(barcode)', #sql的约束表达式
        '订单条码不能重复' #错误提示
    ]
    odoo19之后就不用使用_sql_constraints了，
    推荐使用python的constraint装饰器来实现数据校验
    @api.constrains('field1', 'field2')
    def constraint_barcode(self):
        if record == self:
            domain = [('barcode','=',record.barcode),('id','!=',record.id)]
            if self.search[domain,limit=1]:
                raise ValidationError('订单条码不能重复')


# 搜索方面：
精确匹配
[('name', '=', self)]           # name = 用户输入

模糊匹配
[('name', 'like', self)]        # 区分大小写的模糊匹配
[('name', 'ilike', self)]       # 不区分大小写的模糊匹配 ★常用

数值比较
[('amount', '>', self)]         # 大于
[('amount', '>=', self)]        # 大于等于
[('amount', '<', self)]         # 小于
[('amount', '<=', self)]        # 小于等于

其他
[('name', '!=', self)]          # 不等于
[('id', 'in', self)]            # 在列表中
[('date', 'between', [self1, self2])] # 在日期范围内


# 页面操作
1.返回页面：
    def go_back(self):
        # 这里env是环境变量，env.context是环境变量的上下文，env.context.get()是获取上下文变量的值
        previous_action = self.env.context.get('previous_action_id')
        if previous_action:
            # 这里是通过xml_id获取动作，fore_xml_id是获取xml_id对应的动作
            return self.env['ir.actions.act_window']._for_xml_id(previous_action)
        else:
            # 这里是默认的跳转，跳转到订单列表
            return self.env['ir.actions.act_window']._for_xml_id('test_application.l_sale_order_act_window')

逻辑上是获取上一个动作，然后跳转到上一个动作实现之前的操作

不知道为什么actions_window_close无法使用,然后
 return {
         'type': 'ir.actions.act_window',
         'name': '订单列表',
         'res_model': 'l.sale.order',
         'view_mode': 'list',
         'target': 'main',
     }
强制跳转到主页面也无法使用，打开开发者测试之后在其中开发模块中，明明能搜到这个模块
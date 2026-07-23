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

    -------------------------------------------------------------------------

下面的这个也可以做到，models.Constraint比传统的 _sql_constraints 更易读，且支持多条件组合

    _check_price_unit_positive = models.Constraint(
    
    #这里的 "CHECK(price_unit >= 0)" 就是约束的 定义（definition），它是一个 SQL 表达式，会被原样放进数据库的 CHECK 约束中。
        "CHECK(price_unit >= 0)",
    
    #这里是message字段，报错的时候显示的错误信息
        "单价必须大于0",
    )

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


# 页面操作（7.22）
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

# 小部件(widget)
1.many2many_tax_tags
    many2many_tax_tags: many2many_tax_tags小部件用于many2many字段
        它的作用是把一个多对多字段的显示方式从默认的表格列表，变成标签（tag）样式，
        类似于你常见的“税项标签”，用户可以直接在输入框里添加或删除标签，操作更直观。

    <field name="tax_ids" widget="many2many_tax_tags"/>

2.widget="res_partner_many2one"
    res_partner_many2one: res_partner_many2one小部件用于many2one字段

    widget="res_partner_many2one"
额外提供了一个“卡片预览”功能：当你在输入框里选中一个客户，或者把鼠标悬停在已选客户上时，会弹出一张小卡片，上面显示客户的关键信息（名称、地址、电话、邮箱等），不需要点进表单就能快速查看。

3.default_order=""

    default_order="product_id desc"

写在视图的默认排序

4.widget="handle"
    
    <field name="sequence" widget="handle"/>
如果你拖拽了某一行，数据库中的 sequence 值会被更新，但需要注意的是这个是持久性的，即在关闭窗口后，sequence 值会保存在数据库中。因此，如果你希望在关闭窗口后，sequence 值被重置，你需要在关闭窗口时手动将 sequence 值重置为 0。

5.decoration-{$name}
    decoration-{$name} 是一种特殊样式，用于在字段上添加颜色装饰。
    在 <tree> 或 <list> 视图内的 <field> 元素上添加：

    <field name="field_name" decoration-样式名="条件表达式"/>

样式名 可选：info（蓝色）、success（绿色）、warning（橙色）、danger（红色）、muted（灰色+淡化）、bf（加粗）、it（斜体）等。可叠加多个，如 decoration-success decoration-bf。
条件表达式：任意 Python 布尔表达式，可使用视图内出现的字段名。返回 True 时应用样式。

实例：

    <field name="name" 
       decoration-info="state == 'draft'"
       decoration-success="state == 'confirm'"
       decoration-muted="state == 'done'"/>

6.{'search_default_draft': 1}
    
    {'search_default_draft': 1}

这里 search_default_draft 对应你搜索视图里 <filter name="draft" ...> 的 name
search_default_ 后面必须完全匹配过滤器的 name，区分大小写。
过滤器 name 不要包含特殊字符，最好用英文小写+下划线。
如果 context 中设置了 search_default_xxx，但搜索视图中没有对应的 <filter name="xxx">，前端不会报错，只是没有效果。
动态 context 也可以通过 Python 方法返回 action 时传递
需要注意的是，这个如果不想要了，最好将其留着设定为空值如{}，否则需要重启服务器才会回到不需要筛选的样子
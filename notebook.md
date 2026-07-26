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

    _inherit = ['l.sale.order','l.test.abstract']
需要注意的是这里是创建一个模型的时候此时 l.sale.order 是首次被定义的模型，  
在 Odoo 的注册表（registry）中还不存在，Odoo 就找不到要继承的模型，于是抛出错误。  

如果是已经定义过的表的话那么如下即可

    _inherit = ['l.test.abstract']

经典继承样式：

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
值得注意的是，如果是像下面这样的那么我们再_init_里面需要注意顺序  
如果 model1.py 在 model2.py 之前被导入，  
那么执行到 _inherit = ['model2'] 时，  
Odoo 会去注册表中查找 model1，但此时它还未被注册，  
因此抛出“继承自不存在的模型”错误。  

    class ExtendeModel(models.Model):
        _name = 'new.model'
        _inherit=['model1','model2','model3']

        #继承多个模型的特性

        new_field = fields.Char(string='Combined Field')

为什么必须新建文件，而不是直接修改 Odoo 源码？  
    保护核心代码：升级 Odoo 时不会被覆盖。  
    模块化：可独立安装/卸载，不影响标准功能。  
    可维护性：每个模型单独一个文件，结构清晰。  
    
视图继承如下：（7.24）

    <odoo>
        <record id="view_partner_notebook_form_inherit" model="ir.ui.view">
            <field name="name">res.partner.form.inherit.sale.order</field>
            <field name="model">res.partner</field>
            <field name="inherit_id" ref="base.view_partner_form"/>
            <field name="arch" type="xml">
                <xpath expr="//notebook" position="inside">
                    <page string="销售订单" name="l_sale_order_page">
                        <field name="l_sale_order_ids"/>
                    </page>
                </xpath>
            </field>
        </record>
    </odoo>
    






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

# 向导：  
技术定义：继承自 models.TransientModel 的模型就是向导。它和普通模型（models.Model）很像，有字段、视图、方法。
  
关键区别——数据是临时的：向导记录会保存在数据库的特殊表里，但系统会定期自动清理过期的向导记录（默认保留时间很短），因此它只适合临时存放用户交互过程中的输入，不能用来长期保存业务数据。

1.向导的调用
    
    from odoo import models, fields

    class LSaleOrderWizard(models.TransientModel):
        _name = "l.sale.order.wizard"
        _description = "销售订单向导"         # 建议加上 _description

        name = fields.Char(string="输入内容")
        order_id = fields.Many2one('l.sale.order', string="关联订单")

        def action_confirm(self):
            """点击确认按钮触发的方法"""
            self.ensure_one()
            if self.order_id:
                # 业务逻辑：把向导输入的内容写入订单备注
                self.order_id.note = self.name
            # 关闭向导窗口（注意拼写）
            return {'type': 'ir.actions.act_window_close'}

2.向导的传参：
    
    def action_open_wizard(self):
        self.ensure_one()

        # 通过 XML ID 获取已定义的动作，返回一个字典
        action = self.env['ir.actions.act_window']._for_xml_id(
            'test_application.action_l_sale_order_wizard'
        )

        # 动态注入上下文，把当前订单 ID 传给向导
        action['context'] = {'default_order_id': self.id}
        return action

结构：

    test_application/
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    │   ├── __init__.py
    │   ├── l_sale_order.py
    │   ├── l_sale_order_line.py
    │   ├── l_test_abstract.py
    │   └── ...
    ├── views/
    │   ├── l_sale_order_views.xml
    │   ├── menu_views.xml
    │   └── ...
    ├── wizard/
    │   ├── __init__.py
    │   ├── l_sale_order_wizard.py      # 向导模型
    │   └── l_sale_order_wizard.xml     # 向导视图
    └── security/
        └── ir.model.access.csv


# 模块连接：
1.通过创建“链接模块”，在两个独立的应用之间建立交互，而不破坏各自的独立性。  

背景：  

原有模块 test_application 负责销售订单管理。  
希望当订单完成（状态变为 done）时，自动在会计（account）模块中生成一张客户发票。  

导入依赖  

    from odoo import api, models, fields, Command
    from odoo.exceptions import ValidationError

models：用于定义模型类。  
fields：虽然本文件没有直接定义字段，但导入以备不时之需（可省略）。  
Command：这是核心，用来构建 One2many 字段的创建命令。  
ValidationError：用于在无法创建发票时给出清晰的错误提示。  


继承原有模型  
当用户在界面上点击“完成”按钮时，state_to_done 会被调用。  
super().state_to_done() 首先调用原模块中的 state_to_done 方法，确保状态被正确修改为 'done'。



    class LSaleOrder(models.Model):
        _inherit = "l.sale.order"

重写 state_to_done 方法

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
        <------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        order.line_ids 是销售订单的明细行（One2many 字段），遍历每一行，跳过金额 <=0 的行，
        Command.create({...}) 生成一条“创建新记录”的命令。这个命令会告诉 Odoo：“当创建发票时，请在 invoice_line_ids 字段中创建一条新的发票行记录，字段值如下”。
        
        字段映射：
            name：发票行的描述，优先取产品名，其次取订单行名称，都没有则填“订单行”。
            quantity：数量，直接使用订单行的 qty。
            price_unit：单价，直接使用订单行的 price_unit。
            注意：发票行会自动根据 quantity * price_unit 计算总金额，所以不需要提供 amount_total。
        <------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
            if not line_commands:
                line_commands.append(Command.create({
                    'name':'订单行',
                    'quantity':1,
                    'price_unit':0,
                }))
        <------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        如果所有行都被跳过了（例如全是0元行），至少创建一行占位，避免发票为空。实务中你可能希望直接不创建发票，这里只是示例。


            invoice_vals = {
                'partner_id':order.partner_id.id,
                'move_type':'out_invoice',
                'invoice_line_ids':line_commands,
            }
            invoice = self.env['account.move'].create(invoice_vals)
        partner_id：客户，必须用记录的 ID 或直接传记录集（这里用了 .id 保证清晰）。
        move_type：'out_invoice' 代表客户发票。
        invoice_line_ids：这里是 One2many 字段，直接赋予 Command.create 的命令列表，Odoo 会在创建发票的同时创建这些发票行，并自动将它们关联到该发票。
        self.env['account.move'] 获取 account.move 模型的实例，调用 create 方法在数据库中创建记录。
            

# 看板(kanban):

为什么需要 QWeb？  
文档开篇说，之前的列表和表单视图“设计上没什么可做的”，因为标准视图只是按规则摆放字段。但当你想做这些事时，就需要一个更灵活的工具：  
制作卡片式布局（看板视图）  
生成PDF 报表  
开发网站页面  
这个工具就是 QWeb 模板引擎。它和 Jinja2、Twig 类似，但基于 XML 语法，专门在 Odoo 里生成 HTML。

    <kanban>
        <templates>
            <t t-name="card">
                <div>
                    <field name="name"/>
                </div>
            </t>
        </templates>
    </kanban>

<kanban>：视图类型为看板。  
<templates>：里面可以定义多个 QWeb 模板，看板必须有一个叫 card 的根模板。  
<t t-name="card">：<t> 是 QWeb 指令的占位符，t-name 给这个模板起名为 card。每条记录都会用这个模板渲染出一张卡片。  
<field name="name"/>：在卡片里显示字段 name。

条件显示：t-if 和 record:

    <kanban>
        <field name="state"/>
        <templates>
            <t t-name="card">
                <div>
                    <field name="name"/>
                    <div t-if="record.state.raw_value == 'new'">
                        This is new!
                    </div>
                </div>
            </t>
        </templates>
    </kanban>

需要注意到的是
    record.state.raw_value 是字段 state 的原始值，即 'new'。  
field name="state"写在 templates外面：    
当我们需要用到字段值但不直接显示时，就把字段声明在这里（只加载数据，不渲染 HTML）。这样在模板里就能通过 record 访问它了  
record 对象：每条记录对应的 QWeb 变量。它有：  
    record.field_name.value：根据用户语言/格式处理过的值，适合直接展示。  
    record.field_name.raw_value：数据库原始值（read() 方法拿到的值），适合做逻辑判断  
t-if="条件"：当条件为真时，该元素及其内容才渲染。  

默认分组与拖拽控制：  

    <kanban default_group_by="state" 
            class="o_kanban_small_column"
            quick_create="false"
            on_delete="cascade">
        <!-- quick_create 禁用快速创建 -->
        <!-- on_delete="cascade" 是默认，也可以不写 -->
        ...
    </kanban>

禁止拖拽是通过删除或设置 records_draggable 为 false但在 QWeb 看板里通常通过 CSS 或去掉拖拽句柄实现。  
最简单的办法是添加属性 kanban_draggable="false" 吗？  
实际上标准 Odoo 没有直接属性，但可以通过 <kanban class="o_kanban_no_drag"> 配合自定义 CSS，或者干脆不引入 kanban_draggable 相关的类。  
在 Odoo 14+ 中，可以在 <kanban> 上添加 groups_draggable="false" 和 records_draggable="false"。例如：
    
        <kanban default_group_by="state" 
            records_draggable="false"
            groups_draggable="false">


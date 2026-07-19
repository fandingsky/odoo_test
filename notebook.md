模型的继承：

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
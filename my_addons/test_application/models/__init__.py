# from . import l_test_abstract
# from . import l_sale_order,l_sale_order_line,product_template
# from . import res_partner


from . import l_test_abstract
from . import l_sale_order
from . import l_sale_order_line
from . import product_template
from . import res_partner


# 当 Odoo 加载模块时，它会按照 __init__.py 中的导入顺序加载 Python 文件。


# 如果 l_sale_order.py 在 l_test_abstract.py 之前被导入，
# 那么执行到 _inherit = ['l.test.abstract'] 时，
# Odoo 会去注册表中查找 l.test.abstract，但此时它还未被注册，
# 因此抛出“继承自不存在的模型”错误。
# 当你将一个包作为模块导入时, (import xxx)
# 实际导入的是__init__.py文件, 因此该文件定义了如何导入
# 这个文件控制着包的导入行为. (当然不用python package) 就
# 没有这个文件了,直接导入即可.
# __init__.py中还有一个 __all__列表, 用来管理from package_a import * 的动作
from ch1 import TestNumpyMethod   # 没有这一句,就不能直接import ch1然后通过ch1.TestNumpyMethod来调用模块 TestNumpyMethod里面的内容
__all__ = ["TestNumpyMethod"]



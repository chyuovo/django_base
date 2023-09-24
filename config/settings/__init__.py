# 默认配置
from .base import *

if os.environ.get('ENV', None):
    print("===========当前为生产环境===========")
    from .pro import *
else:
    print("===========当前为开发环境===========")
    from .dev import *
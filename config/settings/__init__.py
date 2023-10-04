# 默认配置
from .base import *

if os.environ.get('ENV', None):
    print("\033[33m ===========当前为生产环境===========\033[0m")
    from .pro import *
else:
    print("\033[33m ===========当前为开发环境===========\033[0m")
    from .dev import *
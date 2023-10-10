"""
系统检查
启动时执行
"""

from django.core.checks import register, Error
import os
@register()
def system_checks(app_configs, **kwargs):
    """
    启动时执行
    """
    print("=================================系统检查=================================")
    if os.environ.get('ENV', None):
        print("\033[33m 1. 当前为生产环境\033[0m")
        
    else:
        print("\033[33m 1. 当前为开发环境\033[0m")
    return []

# @register()
def redis_connection_check(app_configs, **kwargs):
    """
    Redis连接检查
    """
    print("\033[33m 2. Redis 连接检查：\033[0m",end="")
    from django_redis import get_redis_connection
    try:
        connection = get_redis_connection()
        connection.ping()
        print("\033[32m连接成功\033[0m")
        return []
    except Exception as e:
        print("\033[31m连接失败,{}\033[0m".format(str(e)))
        return [Error('Redis 连接失败： {}'.format(str(e)), id='ststem_checks.redis_connection_check')]



@register()
def system_checks_end(app_configs, **kwargs):
    print("=================================检查完成=================================")
    return []

"""
系统检查
启动时执行
"""

from django.core.checks import register, Error

@register()
def redis_connection_check(app_configs, **kwargs):
    """
    Redis连接检查
    """
    print("\033[33mRedis 连接检查：\033[0m",end="")
    from django_redis import get_redis_connection
    try:
        connection = get_redis_connection()
        connection.ping()
        print("\033[32m连接成功\033[0m")
        return []
    except Exception as e:
        print("\033[31m连接失败,{}\033[0m".format(str(e)))
        return [Error('Redis 连接失败： {}'.format(str(e)), id='ststem_checks.E001')]
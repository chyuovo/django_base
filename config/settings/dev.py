DEBUG = True
IF_PERMISSION = True # 是否开启权限控制
ALLOWED_HOSTS = ["*"]# 白名单

# 文件保存设置
import os
MEDIA_ROOT = os.path.join('media') 
MEDIA_URL = "/media/"


"""
数据库配置
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_base',
        'USER': 'root',  # 数据库名字用户名
        'PASSWORD': '123456',  # 数据库密码
        'HOST': '127.0.0.1',
        'PORT': '3306',  # 端口
        'OPTIONS': {'charset': 'utf8mb4'},  # 打开数据库 编码格式 ——解决4字节表情无法储存问题
    }
}


"""
Redis
"""
# CACHES = {
#     "default":{
#         "BACKEND":"django_redis.cache.RedisCache",
#         "LOCATION":"redis://127.0.0.1:6379/0",
#         "OPTIONS":{
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "CONNECTION_POOL_KWARGS": {"max_connections": 100},
#             "PASSWORD": "",
#             "DECODE_RESPONSES": True
#         }
#     }
# }

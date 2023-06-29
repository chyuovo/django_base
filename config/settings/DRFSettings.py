"""
DRF 配置
跨域
"""
from datetime import timedelta
REST_FRAMEWORK = {
    # 分页
    'DEFAULT_PAGINATION_CLASS':  'utils.page.PageNumberPagination',
    # 过滤器
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    # 异常处理
    'EXCEPTION_HANDLER': 'utils.exception_handler.custom_handler',
    # 修改默认返回JSON的renderer的类
    'DEFAULT_RENDERER_CLASSES': ('utils.renderer.CustomRenderer',),
    
    # core api接口文档
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    
    # 时间格式
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    
    # 用户验证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
}

# 登入令牌(Token)设置

REST_KNOX = {
    # 这是授权标头值前缀
    "AUTH_HEADER_PREFIX":"Bearer",
    # 令牌时间   
    'TOKEN_TTL': timedelta(days=30),
    # 每次使用令牌后令牌是否延长时间
    'AUTO_REFRESH': True,
    # 这是更新令牌到期所需的最短时间（以秒为单位） 在数据库中。
    'MIN_REFRESH_INTERVAL':60,
    # 每个用户的令牌限制
    'TOKEN_LIMIT_PER_USER': None,
    'USER_SERIALIZER': 'knox.serializers.UserSerializer',
}

"""解决跨域"""

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True  # 允许所有 域名/IP 跨域
# CORS_ORIGIN_WHITELIST = ('http://127.0.0.1:*',) # 配置可跨域访问的 域名/IP
CORS_ALLOW_METHODS = ('*',)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
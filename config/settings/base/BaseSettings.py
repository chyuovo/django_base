"""
基础配置
"""

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  
    'corsheaders', # 跨域
    'django_apscheduler',# 定时任务
    'rest_framework',  # restful框架
    'django_filters', # 过滤器
    # 'logger', # 日志
    'knox', # 用户认证
    'user' # 用户模块
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'logger.middleware.api_logger_middleware.APILoggerMiddleware',# 日志
]

ROOT_URLCONF = 'urls'

"""语言配置"""
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_TZ =False

# 设置用户模型
AUTH_USER_MODEL = "user.User"


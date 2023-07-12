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
    'corsheaders',
    'rest_framework',
    'django_filters',
    'logger',
    'knox',
    'user'
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
    'logger.middleware.api_logger_middleware.APILoggerMiddleware',
]




# 文件保存设置
import os
MEDIA_ROOT = os.path.join('media') 
MEDIA_URL = "/media/"

DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = 'urls'

"""语言配置"""
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_TZ =False

# 设置用户模型
AUTH_USER_MODEL = "user.User"


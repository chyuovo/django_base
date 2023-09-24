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

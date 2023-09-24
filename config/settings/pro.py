DEBUG = False
ALLOWED_HOSTS = ["*"]# 白名单

# 文件保存设置
import os
MEDIA_ROOT = os.path.join('media') 
MEDIA_URL = "/media/"

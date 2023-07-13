# 日志记录器配置
import os

# drf-api-logger 配置
DRF_API_LOGGER_DATABASE = True # 是否记录到数据库
DRF_API_LOGGER_SIGNAL = True # 是否发送信号
DRF_API_LOGGER_PATH_TYPE = 'ABSOLUTE' # 路径类型 'ABSOLUTE', 'RAW_URI', 'FULL_PATH'
DRF_API_LOGGER_SKIP_URL_NAME = ['log-list'] # 跳过的url
DRF_API_LOGGER_SKIP_NAMESPACE = [] # 跳过的命名空间(应用程序)
DRF_API_LOGGER_METHODS = [] # 跳过的方法
DRF_API_LOGGER_STATUS_CODES = [] # 跳过的状态码
DRF_API_LOGGER_EXCLUDE_KEYS = ['password', 'token', 'access', 'refresh','AUTHORIZATION','COOKIE'] # 在日志中隐藏敏感数据
DRF_LOGGER_QUEUE_MAX_SIZE = 50 # 日志队列最大长度
DRF_LOGGER_QUEUE_FLUSH_INTERVAL = 10 # 日志队列刷新间隔
DRF_API_LOGGER_LOGS_EXPIRE_DAYS = 3 # 日志保存天数

# 日志记录器配置
BASE_DIR = ""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',   
        },

        'general': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/general/general.log',
            'encoding': 'utf-8',
        },
        'info': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/info/info.log',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        "django.server": {
            "level": "INFO",
            "handlers": ["general","console"], 
        },
        '系统日志':{
            'handlers': ['general','console','info'],
            'level': 'INFO',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
}
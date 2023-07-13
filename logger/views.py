from .serializers import APILogsSerializers
from .models import APILogsModel
from rest_framework import viewsets
from rest_framework import permissions
from django.conf import settings
class LogsViewSet(viewsets.ReadOnlyModelViewSet):
    """获取日志列表的视图函数"""
    queryset = APILogsModel.objects.all()
    serializer_class = APILogsSerializers
    permission_classes = [permissions.IsAdminUser]

#  日志清理
import datetime
import logging
logger =  logging.getLogger("系统日志")

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

seconds = settings.DRF_API_LOGGER_LOGS_EXPIRE_DAYS*24*60*60
scheduler = BackgroundScheduler(timezone='Asia/Shanghai') 
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=seconds, args=['日志清理'], id='logger_job1', replace_existing=True)
def logger_job1(name):
    # 查询数据库，将日志保存天数之前的数据删除  
    now = datetime.datetime.now()
    expire_time = now - datetime.timedelta(days=seconds)
    APILogsModel.objects.filter(added_on__lte=expire_time).delete()
    logger.info(f"{name}任务运行成功！,清理了{expire_time}前的日志，当前时间为{now}")

scheduler.start()

# 在DEBUG模式下，启动时运行一次
if settings.DEBUG:
    logger_job1("日志清理")

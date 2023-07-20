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
from datetime import datetime, date, timedelta
import logging
logger =  logging.getLogger("系统日志")

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job
EXPIRE_DAYS = settings.DRF_API_LOGGER_LOGS_EXPIRE_DAYS
scheduler = BackgroundScheduler(timezone='Asia/Shanghai') 
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=EXPIRE_DAYS*24*60*60, args=['日志清理'], id='logger_job1', replace_existing=True)
def logger_job1(name):
    # 查询数据库，将日志保存天数之前的数据删除  
    now = datetime.now()
    expire_time = now -  timedelta(days = EXPIRE_DAYS)
    APILogsModel.objects.filter(added_on__lte=expire_time).delete()
    logger.info(f"{name}任务运行成功！,清理了{expire_time.strftime('%Y-%m-%d %H:%M')}前的日志，当前时间为{now.strftime('%Y-%m-%d %H:%M')}")

# scheduler.start()
# logger_job1("启动时日志清理")
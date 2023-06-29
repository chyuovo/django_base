from .serializers import APILogsSerializers
from .models import APILogsModel
from rest_framework import viewsets
from rest_framework import permissions

class APILogsViewSet(viewsets.ReadOnlyModelViewSet):
    """添加获取日志列表的视图函数"""
    queryset = APILogsModel.objects.all()
    serializer_class = APILogsSerializers
    permission_classes = [permissions.IsAdminUser]

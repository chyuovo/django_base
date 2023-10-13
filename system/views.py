from typing import Any
from django.contrib.auth import get_user_model,password_validation
User = get_user_model()

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import login
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status,mixins
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import  GenericAPIView
from rest_framework.exceptions import AuthenticationFailed,ParseError
from rest_framework.decorators import action

from utils.viewsets import CommonViewSetModel,CommonViewSet,UploadFile,SaveModelMixin

from system.serializers import *
from system.models import *


# Create your views here.
class SystemConfigView(CommonViewSetModel,UploadFile):
    classes_map = {
        'list':{'permissions':[]},
        'retrieve':{'permissions':[]},
        'get_now_config':{'permissions':[]},
        'get_one_config':{'permissions':[]},
        # 'create':{'permissions':[],'serializer':None},
        # 'update':{'permissions':[],'serializer':None},
        # 'partial_update':{'permissions':[],'serializer':None},
        # 'destroy':{'permissions':[],'serializer':None},
    }
    queryset = SystemConfig.objects.all().order_by('-id')
    serializer_class = SystemConfigSerializers
    permission_classes = [permissions.IsAdminUser]
    paper_file = "system/config"
    
    @action(methods=['get'],detail=False)
    def get_now_config(self,request):
        """获取当前配置"""
        configs_key= [
            "USER_VERSION_NUM",
            "STAFF_VERSION_NUM",
            "ADMIN_VERSION_NUM",
            "LOGO"
        ]
        configs = self.queryset.filter(config_name__in=configs_key)
        config_dict = {
            config.config_name: config.config_value
            for config in configs
            if config.is_use
        }
        return Response(config_dict)
    
    @action(methods=['get'],detail=False)
    def get_one_config(self,request):
        """获取单个配置"""
        config_name = request.query_params.get("config_name")
        config = self.queryset.filter(config_name=config_name,is_use=True)
        if config.exists():
            return Response(config.first().config_value)
        return Response(status=status.HTTP_404_NOT_FOUND)

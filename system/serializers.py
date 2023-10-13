from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError,AuthenticationFailed,ParseError
from django.contrib.auth.hashers import make_password
from utils.model_serializer import CommonSerializer
from .models import *
from django.db import transaction

class SystemConfigSerializers(CommonSerializer):
    """ 
    系统配置序列化器 
    """
    is_use = serializers.BooleanField(default=True)
    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ("user",)
    
    def is_set_use(self, validated_data):
        """
        如果有设置为使用,则取消其他使用
        """
        if "is_use" in validated_data and  validated_data['is_use']:
            SystemConfig.objects.filter(config_name = validated_data['config_name'],is_use=True).update(is_use=False)

    @transaction.atomic
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        self.is_set_use(validated_data)
        return super().create(validated_data)
    
    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data["user"] = self.context["request"].user
        self.is_set_use(validated_data)
        return super().update(instance, validated_data)
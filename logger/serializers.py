from .models import APILogsModel
from rest_framework import serializers
import json

class Jsonserializer(serializers.CharField):
    """编写一个序列化字段,将字符串转为json对象"""
    def to_representation(self, value):
        try:
            return json.loads(value)
        except Exception as e:
            return value
        

class APILogsSerializers(serializers.ModelSerializer):
    # 将json字符串转为json对象，方便前端展示，否则前端展示的是字符串

    headers = Jsonserializer()
    body = Jsonserializer()
    response = Jsonserializer()
    
    class Meta:
        model = APILogsModel
        fields = '__all__'
        
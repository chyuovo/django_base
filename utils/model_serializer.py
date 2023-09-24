from rest_framework import serializers
from rest_framework.fields import empty

class CommonSerializer(serializers.ModelSerializer):
    many = False
    many_exclude = [] # 多个时,需要排除的字段
    def __init__(self, instance=None, data=empty, **kwargs):
        if isinstance(instance, list):
            self.many = True
        super().__init__(instance, data, **kwargs)
    
    def get_fields(self):
        fields = super().get_fields()
        if self.many:
            for field in self.many_exclude:
                fields.pop(field)
        return fields

        
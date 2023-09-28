from rest_framework import serializers
from rest_framework.fields import empty

class CommonSerializer(serializers.ModelSerializer):
    """
    字段排除
    同时使用时，将会采用基础时的排除
    base_exclude: 基础时,需要排除的字段
    many_exclude: 多个时,需要排除的字段
    """
    
    base = False
    base_exclude = [] # 基础时,需要排除的字段

    many = False
    many_exclude = [] # 多个时,需要排除的字段

    

    def __init__(self, instance=None, data=empty, **kwargs):
        print(kwargs.get('base',False))
        self.base = kwargs.pop('base',False)
        if isinstance(instance, list):
            self.many = True
        super().__init__(instance, data, **kwargs)
    
    def get_fields(self):
        fields = super().get_fields()
        if self.base:
            for field in self.base_exclude:
                fields.pop(field)
        elif self.many:
            for field in self.many_exclude:
                fields.pop(field)
        return fields

        
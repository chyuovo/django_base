from rest_framework import serializers
from rest_framework.fields import empty

class CommonSerializer(serializers.ModelSerializer):
    """
        字段排除
        同时使用时，将会采用基础时的排除
        必须保证字段存在
        base_fields: 基础时，需要返回的字段(优先级1)
        base_exclude: 基础时,需要排除的字段(优先级2)
        many_exclude: 多个时,需要排除的字段(优先级3)
    """
    
    base = False
    base_fields = []   # 基础时，需要返回的字段(优先使用)
    base_exclude = [] # 基础时,需要排除的字段

    many = False
    many_exclude = [] # 多个时,需要排除的字段
    
    def __init__(self, instance=None, data=empty, **kwargs):
        self.base = kwargs.pop('base',False)
        self.base_fields = kwargs.pop('base_fields', self.base_fields)
        self.base_exclude = kwargs.pop('base_fields', self.base_exclude)
        if isinstance(instance, list):
            self.many = True
        super().__init__(instance, data, **kwargs)
    
    def get_fields(self):
        fields = super().get_fields()
        if self.base:
            if len(self.base_fields)>0:
                fields_copy = fields.copy()
                for field in fields_copy:
                    if field not in self.base_fields:
                        fields.pop(field)
            else:
                for field in self.base_exclude:
                    fields.pop(field)
        elif self.many:
            for field in self.many_exclude:
                fields.pop(field)
        return fields
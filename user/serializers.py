from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from django.contrib.auth.hashers import make_password

class UserSerializers(serializers.ModelSerializer):
    """ 
    用户序列化器 
    """
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user =  super().create(validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    """
    登入序列化器
    """
    password = serializers.CharField(required=True, style={"input_type": "password"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField(required=True)
        
    def validate(self, attrs):
        password = attrs.get("password")
        params = {User.USERNAME_FIELD: attrs.get(User.USERNAME_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )

        if not self.user:
            self.user = User.objects.filter(**params).first()
            if not self.user:
                raise AuthenticationFailed("用户不存在")
                
            if self.user and not self.user.check_password(password):
                raise AuthenticationFailed("账户或密码错误")
        
        if self.user and self.user.is_active:
            attrs['user'] = self.user
            return attrs
        
        raise AuthenticationFailed("账户已冻结")
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError,AuthenticationFailed,ParseError
from django.contrib.auth.hashers import make_password
class UserSerializers(serializers.ModelSerializer):
    """ 
    管理员用户序列化器 
    默认密码为登入账户
    """
    class Meta:
        model = User
        exclude = ('password',)
    
    def create(self, validated_data):
        """设置密码为账户名"""
        validated_data["password"] = make_password(validated_data[User.USERNAME_FIELD])
        return super().create(validated_data)

class BaseUserSerializers(serializers.ModelSerializer):
    """ 
    用户序列化器
    """
    class Meta:
        model = User
        exclude = ['password']
        read_only_fields=['groups','department','is_superuser','is_active','is_staff','user_permissions','last_login','date_joined']

class RegisterSerializers(serializers.ModelSerializer):
    """ 
    注册序列化器
    """
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        exclude = ['groups','is_superuser','is_active','is_staff','user_permissions','last_login','date_joined']
        
    def create(self, validated_data):
        """加密密码"""
        validated_data["password"] = make_password(validated_data["password"]) 
        return super().create(validated_data)

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
        """验证账户密码"""
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

class SetPasswordSerializer(serializers.Serializer):
    """ 设置密码序列化器 """
    old_password =  serializers.CharField(required=True, style={"input_type": "password"})
    new_password1 =  serializers.CharField(required=True, style={"input_type": "password"})
    new_password2 =  serializers.CharField(required=True, style={"input_type": "password"})

    def validate(self, attrs):
        request=self.context.get("request")
        if attrs.get("new_password1") != attrs.get("new_password2"):
            raise ParseError("两次输入的密码不一致")
        
        if not request.user.check_password(attrs.get("old_password")):
            raise ParseError("旧密码不正确")

        if attrs.get("old_password") == attrs.get("new_password1"):
            raise ParseError("新密码不能与旧密码相同")
        
        return attrs



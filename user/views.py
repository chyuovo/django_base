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

from knox.models import AuthToken
from knox import views as knox_views
from utils.viewsets import CommonViewSetModel,CommonViewSet,UploadFile,SaveModelMixin

from .serializers import *
from .filter import UserFilter


"""
登入处理
self: 继承knox_views后的对象
request: 请求
user: 登入的用户
"""
def login_user(self,request, user):
    # 令牌数量验证
    token_limit_per_user = self.get_token_limit_per_user()

    if token_limit_per_user is not None:
        now = timezone.now()
        token = user.auth_token_set.filter(expiry__gt=now).order_by('-expiry')
        if settings.REST_KNOX["TOKEN_LIMIT_PER_USER_IS_DELETED"]:
            try:   
                # 删除多余的令牌
                print(len(token[token_limit_per_user-1:]))
                for i in token[token_limit_per_user-1:]:
                    i.delete()
            except TypeError:
                pass

        else:
            if token.count() >= token_limit_per_user:
                raise AuthenticationFailed("登入设备超过上限")
    
    token_ttl = self.get_token_ttl()
    instance, token = AuthToken.objects.create(user, token_ttl)
    user_logged_in.send(sender=user.__class__,
                        request=request, user=user)
    data = self.get_post_response_data(request, token, instance)
    return Response({**data,"user":UserSerializers(user,base=True).data})

class LoginView(knox_views.LoginView,GenericAPIView):
    """
    登入视图
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer


    def post(self, request):    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        request.user = user
        # login(request, user)
        return login_user(self,request, user)

    


class LogoutView(knox_views.LogoutView):
    """
    重写登出视图，返回200状态码
    """
    def post(self, request, format=None):
        super().post(request,format)
        return Response(status=status.HTTP_200_OK)

class LogoutAllView(knox_views.LogoutAllView):
    """
    重写登出所有视图，返回200状态码
    """
    def post(self, request, format=None):
        super().post(request,format)
        return Response(status=status.HTTP_200_OK)

class AdminUserView(CommonViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,SaveModelMixin):
    # 修改list及retrieve权限
    classes_map = {
        # 'list':{'permissions':[]},
        # 'retrieve':{'permissions':[]},
    }

    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAdminUser]
    filterset_class  = UserFilter

    @action(methods=['put'],detail=True,url_path="reset_password")
    def reset_password(self,request,pk):
        """
        重置密码为账户
        """
        user:User = self.get_object()
        user.set_password(getattr(user,User.USERNAME_FIELD))
        user.save()
        user.auth_token_set.all().delete()
        return Response()
    
    @action(methods=['put'],detail=False,url_path="disable")
    def disable(self,request):
        """批量禁用用户"""
        ids = request.data.get("ids")
        if ids is None:
            raise ParseError("未提供ids")
        self.queryset.filter(pk__in=ids).update(is_active=False)
        return Response()
    
    @action(methods=['put'],detail=False,url_path="enable")
    def enable(self,request):
        """批量激活用户"""
        ids = request.data.get("ids")
        if ids is None:
            raise ParseError("未提供ids")
        self.queryset.filter(pk__in=ids).update(is_active=True)
        return Response()

    @action(methods=['put'],detail=True,url_path="active")
    def active(self,request,pk):
        """激活或禁用用户,返回用户信息"""
        user:User = self.get_object()
        if request.data.get("is_active") is None:
            raise ParseError("未提供is_active")
        user.is_active = request.data.get("is_active")
        user.save()
        return Response(self.get_serializer(user).data)
    
    @action(methods=['put'],detail=True,url_path="is_staff")
    def is_staff(self,request,pk):
        """设置或取消用户管理员身份"""
        user:User = self.get_object()
        if request.data.get("is_staff") is None:
            raise ParseError("未提供is_staff")
        user.is_staff = request.data.get("is_staff")
        user.save()
        return Response(self.get_serializer(user).data)
    
    @action(methods=['put'],detail=True,url_path="is_superuser")
    def is_superuser(self,request,pk):
        """设置或取消用户超级管理员身份"""
        user:User = self.get_object()
        if request.data.get("is_superuser") is None:
            raise ParseError("未提供is_superuser")
        user.is_superuser = request.data.get("is_superuser")
        user.save()
        return Response(self.get_serializer(user).data)



class UserView(CommonViewSet,UploadFile):
    """
    用户
    """
    classes_map = {
        'upload_file':{'permissions':[permissions.IsAuthenticated],'serializer':None},
        'getMe':{'permissions':[permissions.IsAuthenticated],'serializer':BaseUserSerializers},
        'set_password':{'permissions':[permissions.IsAuthenticated],'serializer':SetPasswordSerializer},
        'update_profile':{'permissions':[permissions.IsAuthenticated],'serializer':BaseUserSerializers},
        'register':{'permissions':[],'serializer':RegisterSerializers},
    }
    
    queryset = User.objects.all()
    serializer_class = BaseUserSerializers
    permission_classes = [permissions.IsAuthenticated]
    # 头像
    paper_file = "avatars"
    user_unique_file = True
    file_type = ["jpeg","GIF","JPG","PNG"]

    @action(methods=['get'],detail=False,url_path="me")
    def getMe(self,request):
        return Response(self.get_serializer(request.user).data)

    
    @action(methods=['post'],detail=False,url_path="set_password")
    def set_password(self,request):
        """设置密码"""
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            password_validation.validate_password(request.data["new_password1"],request.user)
        except DjangoValidationError as e:
            raise ParseError(list(e)[0])
        
        request.user.set_password(request.data["new_password1"])
        request.user.save()
        request.user.auth_token_set.all().delete()
        return Response()  

    
    @action(methods=['put'],detail=False,url_path="update_profile")
    def update_profile(self,request, *args, **kwargs):
        """修改个人信息"""
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
    @action(methods=['post'],detail=False,url_path="register")
    def register(self,request, *args, **kwargs):
        """用户注册"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from typing import Any
from django.contrib.auth import get_user_model,password_validation
User = get_user_model()

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import login
from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status,mixins
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import  GenericAPIView
from rest_framework.exceptions import AuthenticationFailed,ParseError
from rest_framework.decorators import action

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from utils.viewsets import CommonViewSetModel,CommonViewSet,UploadFile


from .serializers import *
from .models import Department
from .filter import UserFilter,DepartmentFilter

class LoginView(KnoxLoginView,GenericAPIView):
    """
    登入视图
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                raise AuthenticationFailed("登入设备超过上限")
            
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        return Response({**data,"user":UserSerializers(user).data})



class AdminUserView(CommonViewSetModel):
    # 修改list及retrieve权限
    classes_map = {
        'list':{'permissions':[]},
        'retrieve':{'permissions':[]},
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
        return Response()

    @action(methods=['put'],detail=True,url_path="active")
    def active(self,request,pk):
        """激活或禁用用户,返回用户信息"""
        user:User = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response(self.get_serializer(user).data)
    
    @action(methods=['put'],detail=True,url_path="is_staff")
    def is_staff(self,request,pk):
        """设置或取消用户管理员身份"""
        user:User = self.get_object()
        user.is_staff = not user.is_staff
        user.save()
        return Response(self.get_serializer(user).data)
    
    @action(methods=['put'],detail=True,url_path="is_superuser")
    def is_superuser(self,request,pk):
        """设置或取消用户超级管理员身份"""
        user:User = self.get_object()
        user.is_superuser = not user.is_superuser
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


class DepartmentView(CommonViewSetModel,UploadFile):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class  = DepartmentFilter

    # 部门lOGO保存信息
    paper_file = "department"
    user_unique_file = True
    file_type = ["jpeg","GIF","JPG","PNG"]


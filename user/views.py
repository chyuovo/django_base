from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import login
from django.utils import timezone

from rest_framework import status,mixins
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import  GenericAPIView
from rest_framework.exceptions import AuthenticationFailed

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from utils import CommonViewSetModel,UploadFile
from .serializers import UserSerializers,LoginSerializer

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



class UserView(CommonViewSetModel,UploadFile):
    
    permission_classes_map = {
        "list":[permissions.IsAdminUser],
        "retrieve":[permissions.IsAdminUser],
        "create":[permissions.IsAdminUser],
        "update":[permissions.IsAdminUser],
        "partial_update":[permissions.IsAdminUser],
        "destroy":[permissions.IsAdminUser],
    }
    queryset = User.objects.all()
    serializer_class = UserSerializers
    # 头像
    paper_file = "avatars"
    user_unique_file = True
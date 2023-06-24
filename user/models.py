from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('必须设置手机号码')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    phone = models.CharField("手机号",max_length=15, unique=True)
    real_name = models.CharField("真实姓名",max_length=150, blank=True)
    username = models.CharField("用户名",max_length=150,blank=True)
    avatar = models.CharField("头像",max_length=150, null=True, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    
    def __str__(self):
        return f"phone:{self.phone}、first_name:{self.first_name}"
    
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
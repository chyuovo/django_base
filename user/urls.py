from django.urls import path
from rest_framework import routers
router = routers.DefaultRouter()
from . import views

router.register("user",views.UserView,"me")
router.register("admin/user",views.AdminUserView,"user")


urlpatterns = [
    path('auth/login/', views.LoginView.as_view(), name='knox_login'),
    path('auth/logout/', views.LogoutView.as_view(), name='knox_logout'),
    path('auth/logoutall/', views.LogoutAllView.as_view(), name='knox_logoutall'),
]

urlpatterns += router.urls
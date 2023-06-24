from django.urls import path
from rest_framework import routers
router = routers.DefaultRouter()
from . import views

router.register("user",views.UserView,"user")

from knox import views as knox_views
from .views import LoginView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='knox_login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]

urlpatterns += router.urls
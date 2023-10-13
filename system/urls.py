from django.urls import path
from rest_framework import routers
router = routers.DefaultRouter()
from . import views

router.register("systemconfig",views.SystemConfigView,"systemconfig")

urlpatterns = [
]

urlpatterns += router.urls
from django.urls import path
from rest_framework import routers
router = routers.DefaultRouter()
from . import views

router.register("log",views.LogsViewSet,"log")

urlpatterns = []

urlpatterns += router.urls
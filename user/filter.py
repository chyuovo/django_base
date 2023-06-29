from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Department


class UserFilter(filters.FilterSet):
    """
    用户过滤器
    username: 模糊查询用户名
    department:筛选部门编号，多选
    department_name:模糊查询部门名称
    real_name:模糊查询真实姓名
    """
    username = filters.CharFilter(field_name='username', lookup_expr="icontains")
    department = filters.ModelMultipleChoiceFilter(queryset=Department.objects.all())
    real_name = filters.CharFilter(field_name='real_name', lookup_expr="icontains")
    department_name = filters.CharFilter(field_name='department__name', lookup_expr="icontains")
    
    class Meta:
        model = User
        fields = ("username","department")

class DepartmentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr="icontains")
    class Meta:
        model = Department
        fields = ("name",)
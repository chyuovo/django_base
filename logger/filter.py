from django_filters import rest_framework as filters
from .models import APILogsModel

class APILogsFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user', lookup_expr="icontains")
    method = filters.ModelMultipleChoiceFilter(queryset=APILogsModel.objects.all())
    status_code = filters.ModelMultipleChoiceFilter(queryset=APILogsModel.objects.all())
    class Meta:
        model = APILogsModel
        fields = ("user","method","status_code",)

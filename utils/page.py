"""
全局分页信息
"""
from rest_framework.pagination import PageNumberPagination
class PageNumberPagination(PageNumberPagination):
    page_size = 10  # 每页显示3条数据
    page_query_param = 'page_index'  # 查询参数
    page_size_query_param = 'page_size'
    max_page_size = 100  # 最大每页显示五条数据

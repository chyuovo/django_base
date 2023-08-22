"""
全局分页信息
"""

from rest_framework.pagination import PageNumberPagination
class PageNumberPagination(PageNumberPagination):
    # 默认单页数量
    page_size = 10  
    # 页数参数
    page_query_param = 'pageIndex' 
    # 单页数量
    page_size_query_param = 'pageSize'
    # 最大数量
    max_page_size = 100

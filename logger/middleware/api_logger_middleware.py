import json,re,time

from django.conf import settings
from django.urls import resolve
from django.utils import timezone

from logger import API_LOGGER_SIGNAL
from logger.utils.start_logger_when_server_starts import LOGGER_THREAD
from logger.utils.utils import get_headers, get_client_ip, mask_sensitive_data

from knox.auth import TokenAuthentication
from rest_framework import exceptions



"""
File: api_logger_middleware.py
Class: APILoggerMiddleware
重写以在日志中记录用户信息
"""


class APILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 一次性配置和初始化。
        self.DRF_API_LOGGER_DATABASE = settings.DRF_API_LOGGER_DATABASE
        self.DRF_API_LOGGER_SIGNAL = settings.DRF_API_LOGGER_SIGNAL
        self.DRF_API_LOGGER_PATH_TYPE = settings.DRF_API_LOGGER_PATH_TYPE
        self.DRF_API_LOGGER_SKIP_URL_NAME = settings.DRF_API_LOGGER_SKIP_URL_NAME
        self.DRF_API_LOGGER_SKIP_NAMESPACE = settings.DRF_API_LOGGER_SKIP_NAMESPACE
        self.DRF_API_LOGGER_METHODS = settings.DRF_API_LOGGER_METHODS
        self.DRF_API_LOGGER_STATUS_CODES = settings.DRF_API_LOGGER_STATUS_CODES

    def __call__(self, request):
        # 只在启用logger时运行
        if self.DRF_API_LOGGER_DATABASE or self.DRF_API_LOGGER_SIGNAL:
            url_name = resolve(request.path_info).url_name
            namespace = resolve(request.path_info).namespace

            # 总是跳过管理面板
            if namespace == 'admin':
                return self.get_response(request)

            # 跳过url名称            
            if url_name in self.DRF_API_LOGGER_SKIP_URL_NAME:
                if settings.DEBUG:
                    print("url_name：",url_name,"该接口不记录")
                return self.get_response(request)
            if settings.DEBUG:
                print("url_name：",url_name)
            
            # 使用命名空间跳过整个应用
            if namespace in self.DRF_API_LOGGER_SKIP_NAMESPACE:
                return self.get_response(request)

            start_time = time.time()
            request_data = ''
            try:
                request_data = json.loads(request.body) if request.body else ''
            except:
                pass
            if settings.DEBUG:
                print("请求体：",request_data)
            #之前每个请求要执行的代码
            #调用视图(以及之后的中间件)。
            response = self.get_response(request)

            # Only log required status codes if matching
            if self.DRF_API_LOGGER_STATUS_CODES and response.status_code not in self.DRF_API_LOGGER_STATUS_CODES:
                return response

            # 如果匹配，只记录所需的状态码
            # 视图被调用。
            headers = get_headers(request=request)
            method = request.method

            # 如果可用，只记录已注册的方法。
            if len(self.DRF_API_LOGGER_METHODS) > 0 and method not in self.DRF_API_LOGGER_METHODS:
                return response

            if response.get('content-type') in ('application/json', 'application/vnd.api+json', 'application/gzip'):
                
                if response.get('content-type') == 'application/gzip':
                    response_body = '** GZIP Archive **'
                elif getattr(response, 'streaming', False):
                    response_body = '** Streaming **'
                else:
                    if type(response.content) == bytes:
                        response_body = json.loads(response.content.decode())
                    else:
                        response_body = json.loads(response.content)
                if self.DRF_API_LOGGER_PATH_TYPE == 'ABSOLUTE':
                    api = request.build_absolute_uri()
                elif self.DRF_API_LOGGER_PATH_TYPE == 'FULL_PATH':
                    api = request.get_full_path()
                elif self.DRF_API_LOGGER_PATH_TYPE == 'RAW_URI':
                    api = request.get_raw_uri()
                else:
                    api = request.build_absolute_uri()
                
                
                try:
                    user,_ = TokenAuthentication().authenticate(request)
                except Exception as e: 
                    user = None
                
                data = dict(
                    user=user,
                    api=mask_sensitive_data(api, mask_api_parameters=True),
                    headers=mask_sensitive_data(headers),
                    body=mask_sensitive_data(request_data),
                    method=method,
                    client_ip_address=get_client_ip(request),
                    response=mask_sensitive_data(response_body),
                    status_code=response.status_code,
                    execution_time=time.time() - start_time,
                    added_on=timezone.now()
                )
                if self.DRF_API_LOGGER_DATABASE:
                    if LOGGER_THREAD:
                        d = data.copy()
                        d['headers'] = json.dumps(d['headers'], indent=4, ensure_ascii=False)
                        if request_data:
                            d['body'] = json.dumps(d['body'], indent=4, ensure_ascii=False)
                        d['response'] = json.dumps(d['response'], indent=4, ensure_ascii=False)
                        LOGGER_THREAD.put_log_data(data=d)
                if self.DRF_API_LOGGER_SIGNAL:
                    API_LOGGER_SIGNAL.listen(**data)
            else:
                return response
        else:
            response = self.get_response(request)
        return response

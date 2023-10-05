from rest_framework.views import exception_handler
from rest_framework.views import Response
from rest_framework import status
from django.conf import settings
from .str_utils import clean_space
from rest_framework.exceptions import ValidationError
# 错误处理（有错误）
def custom_handler(err,context: dict):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    
    response = exception_handler(err, context)
    if response is None:
        # 在DEBUG模式下不处理系统异常,如果处理后错误页面将变成标准格式
        if settings.DEBUG:
            raise err
        res = {'msg': f'服务器错误:{err}','code':500}
        return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    else:
        msg = response.reason_phrase
        code = response.status_code
        # 429 请求频繁
        if code == 429:
            msg = "请求频繁"
        
        elif isinstance(err,ValidationError):
            code = 4000
            # 取出首个错误
            for k,v in response.data.items():  
                msg = v
                if isinstance(v,list):
                    msg = v[0]

        elif "detail" in response.data:
            msg = response.data["detail"]
        else:
            print(err)
            msg = "未知异常"

        res = {}
        res.update(response.data)
        res["msg"] = clean_space(msg)
        res["code"] = code
        return Response(res, status=response.status_code, exception=True)
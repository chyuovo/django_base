from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import hashlib,os
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
class CommonViewSet(GenericViewSet):
    '''
    该视图类灵活配置权限映射
    重新定义方法的返回值
    '''
    permission_classes_map = {
        # "list":[IsAdminUser],
        # "retrieve":[IsAdminUser],
        # "create":[IsAdminUser],
        # "update":[IsAdminUser],
        # "partial_update":[IsAdminUser],
        # "destroy":[IsAdminUser],
    }
    def initial(self, request, *args, **kwargs):
        """重新定义此方法，添加灵活配置权限映射"""
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        
        if hasattr(handler, '__name__'):
            handler_name = handler.__name__
        elif hasattr(handler, '__func__'):
            handler_name = handler.__func__.__name__
        else:
            handler_name = None
        
        if handler_name and handler_name in self.permission_classes_map:
            if isinstance(self.permission_classes_map.get(handler_name), (tuple, list)):
                self.permission_classes = self.permission_classes_map.get(handler_name)
        return super(GenericViewSet, self).initial(request, *args, **kwargs)


class CommonViewSetModel(CommonViewSet,ModelViewSet):
    """
    viewset提供了默认的方法
    """
    pass



    


class UploadFile(CommonViewSet):
    """
    通过Hash值+文件大小+文件最后修改时间命名保存文件
    """

    # 文件保存的二级目录
    paper_file = "common"
    # 文件是否以登入字段命名（即每个用户唯一）
    user_unique_file = False

    @action(methods=['post'],detail=False,url_path="upload")
    def add_file(self,request):
        file_obj = request.FILES.get('file')    # 获取文件
        file_data = file_obj.file.read()        #读取文件
        # {os.path.splitext(file_obj.name)[1]}
        if not self.user_unique_file:
            m = hashlib.md5()   #创建md5对象
            m.update(file_data)  #更新md5对象
            file_hash = m.hexdigest() #哈希值
            filename = f"{file_hash}{file_obj.size}{file_obj.name}"
        else:
            if not request.user.pk:
                raise AuthenticationFailed("身份认证信息未提供。")
            filename = f"{request.user.phone}{os.path.splitext(file_obj.name)[1]}"
            
        filename = os.path.join(settings.MEDIA_ROOT,self.paper_file,filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'wb') as f:
            f.write(file_data)
        return Response({"url":'/'+filename.replace('\\', '/')})
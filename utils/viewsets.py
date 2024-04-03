from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import hashlib,os
from django.conf import settings
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ParseError,AuthenticationFailed
from django.db import transaction


class CommonViewSet(GenericViewSet):
    '''
    该视图类灵活配置权限映射
    重新定义方法的返回值
    '''

    classes_map = {
        # 'list':{'permissions':[],'serializer':None},
        # 'retrieve':{'permissions':[],'serializer':None},
        # 'create':{'permissions':[],'serializer':None},
        # 'update':{'permissions':[],'serializer':None},
        # 'partial_update':{'permissions':[],'serializer':None},
        # 'destroy':{'permissions':[],'serializer':None},
    }
    
    def initial(self, request, *args, **kwargs):
        """重新定义此方法，添加灵活配置权限映射"""
        if not settings.IF_PERMISSION:
            print("注意：权限验证已关闭")
            self.permission_classes = []
            return super(GenericViewSet, self).initial(request, *args, **kwargs)
        handler_name = self.action
        if handler_name and handler_name in self.classes_map:
            if isinstance(self.classes_map.get(handler_name).get('permissions'), (tuple, list)):
                self.permission_classes = self.classes_map.get(handler_name).get('permissions')
        return super(GenericViewSet, self).initial(request, *args, **kwargs)

    def get_serializer_class(self):
        """重新定义此方法，实现灵活配置序列化器"""
        handler_name = self.action
        if handler_name and handler_name in self.classes_map:
            if  self.classes_map.get(handler_name).get("serializer") is not None:
                self.serializer_class = self.classes_map.get(handler_name).get("serializer")
                
        return super().get_serializer_class()
    
    def response_page(self,queryset,request):
        """
        快速分页方法，需要结果集和请求对象
        """
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True,context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)


class DeleteModelMixin:
    """多删，post请求，参数为ids数组"""

    @transaction.atomic
    @action(methods=['post'],detail=False,url_path="delete")
    def delete(self,request):
        ids = request.data.get("ids")
        if ids is None:
            raise ParseError("未提供ids")
        for i in self.queryset.filter(pk__in=ids):
            self.perform_destroy(i)
        return Response()

class SaveModelMixin:
    """
    save方法，实现自定义保存逻辑
    post 请求
    在请求体中有id则则更新，无id则新增，允许部分更新
    """
    @action(methods=['post'],detail=False,url_path="save")
    def save(self,request):
        instance = None
        if request.data.get("id"):
            instance = self.queryset.get(pk=request.data.get("id"))
        serializer = self.get_serializer(instance,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommonViewSetModel(CommonViewSet,ModelViewSet,DeleteModelMixin,SaveModelMixin):
    """
    viewset提供了默认的
    `create()`, `retrieve()`, 
    `update()`,`partial_update()`, `destroy()`,
    `list()`,`delete()`,`save()`操作
    """
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response()



    


class UploadFile():
    """
    通过Hash值+文件大小+文件最后修改时间命名保存文件
    用户唯一文件将所有用户id命名
    """

    # 文件保存的二级目录
    paper_file = "common"
    # 文件是否以Hash值+文件大小+文件最后修改时间命名
    # 如果为False则不修改文件名字(重名将被覆盖)
    hash_file = True
    # 文件是否以登入字段命名（即每个用户唯一）
    user_unique_file = False
    # 允许上传的文件类型
    file_type = []
    
    def file_format_validator(self,upload_file):
        """
        验证文件格式是否为数组中的文件格式
        文件后缀不区分大小写
        :param filename: 文件名  
        :param file_type: 文件类型数组 
        """
        if len(self.file_type) == 0:
            return
        validator =  FileExtensionValidator(self.file_type)
        try:
            validator(upload_file)
        except ValidationError as e:
            print(e)
            raise ParseError(f"文件类型不被允许，允许的类型为{'、'.join(self.file_type)}")


    @action(methods=['post'],detail=False,url_path="upload")
    def upload_file(self,request):
        upload_file = request.FILES.get('file')    # 获取文件
        if upload_file is None:
            raise ParseError("未上传文件")
        file_data = upload_file.file.read()        #读取文件
        self.file_format_validator(upload_file)

        if self.user_unique_file:
            "用户唯一文件将所有用户id命名"
            if not request.user.pk:
                raise AuthenticationFailed("身份认证信息未提供。")
            filename = f"{request.user.pk}{os.path.splitext(upload_file.name)[1]}"
        elif self.hash_file:
            "通过Hash值+文件大小+文件最后修改时间命名保存文件"
            
            m = hashlib.md5()   #创建md5对象
            m.update(file_data)  #更新md5对象
            file_hash = m.hexdigest() #哈希值
            filename = f"{file_hash}{upload_file.size}{upload_file.name}"
        else:
            "文件原名保存"
            filename = f"{upload_file.name}"
        # if not self.user_unique_file:
        #     m = hashlib.md5()   #创建md5对象
        #     m.update(file_data)  #更新md5对象
        #     file_hash = m.hexdigest() #哈希值
        #     filename = f"{file_hash}{upload_file.size}{upload_file.name}"
        # else:
        #     if not request.user.pk:
        #         raise AuthenticationFailed("身份认证信息未提供。")
        #     filename = f"{request.user.pk}{os.path.splitext(upload_file.name)[1]}"
            
        filepath = os.path.join(settings.MEDIA_ROOT,self.paper_file,filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(file_data)
        filename = f"{settings.MEDIA_URL}{self.paper_file}/{filename}"
        return Response({"url":filename.replace('\\', '/')})
from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import hashlib,os
from django.conf import settings
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ParseError,AuthenticationFailed



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

class CommonViewSetModel(CommonViewSet,ModelViewSet):
    """
    viewset提供了默认的方法
    """
    pass



    


class UploadFile():
    """
    通过Hash值+文件大小+文件最后修改时间命名保存文件
    用户唯一文件将所有用户id命名
    """

    # 文件保存的二级目录
    paper_file = "common"
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
        file_data = upload_file.file.read()        #读取文件

        self.file_format_validator(upload_file)
        
        if not self.user_unique_file:
            m = hashlib.md5()   #创建md5对象
            m.update(file_data)  #更新md5对象
            file_hash = m.hexdigest() #哈希值
            filename = f"{file_hash}{upload_file.size}{upload_file.name}"
        else:
            if not request.user.pk:
                raise AuthenticationFailed("身份认证信息未提供。")
            filename = f"{request.user.pk}{os.path.splitext(upload_file.name)[1]}"
            
        filepath = os.path.join(settings.MEDIA_ROOT,self.paper_file,filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(file_data)
        filename = f"{settings.MEDIA_URL}{self.paper_file}/{filename}"
        return Response({"url":filename.replace('\\', '/')})
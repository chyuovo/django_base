# 项目说明

## 配置文件运行

```shell
# 开发模式
python manage.py runserver
# 生成模式
# window
cmd /V /C "set ENV=production && python manage.py runserver"
# Linux
ENV=production python manage.py runserver
```

## 相关依赖

1. [Django 中文文档](https://docs.djangoproject.com/zh-hans/4.2/)
2. [Django REST framework 中文文档](https://q1mi.github.io/Django-REST-framework-documentation/)
3. [Django-Rest-Knox](https://james1345.github.io/django-rest-knox/)
4. [django-filter](https://django-filter.readthedocs.io/en/main/guide/usage.html#the-filter)
5. [drf_api_logger](https://pypi.org/project/drf-api-logger/)

## 常用命令

```shell
pipreqs ./ --encoding=utf

# 镜像安装某个包
pip install django-filters --index-url=https://mirrors.aliyun.com/pypi/simple/

# 依赖管理
pip freeze > requirements.txt
pip install --index-url=https://mirrors.aliyun.com/pypi/simple/ -r requirements-my.txt

# 数据库
python manage.py makemigrations
python manage.py migrate

# 创建
django-admin startproject xxx
python manage.py startapp xxx
python manage.py createsuperuser

# 启动
python manage.py runserver

# admin
# pbkdf2_sha256$600000$t6Q3ICldoEeO3qkgzxFugQ$FqbvYpNwfmQH0yQEXVq3MdiYQO9QtRUNJvXQ21dxuMI=
```

## 修改内容

1. 统一返回格式{msg:'',code:'',data:''}
2. 修改视图集(utils/viewsets)
    - 增加快速分页方法
    - 增加多删接口
    - 允许灵活配置序列化器(方便默认api接口文档显示)，
    - 允许灵活配置权限映射
    - 增加文件处理接口类(utils/viewsets/UploadFile)
3. 完成错误处理返回
4. 通过`Django-Rest-Knox`完成认证，修改退出登入状态码为200
5. 重写用户模型(user/models)

## 更新记录

- 2023-10-05 CY
    1. 增加默认限流，处理限流信息
    2. Token上限后默认采用删除最先过期的Token
    3. 修改及重置密码后删除所有Token

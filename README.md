# DRF

## Token Authentication(令牌认证)

在 Header 添加参数 Authorization，其值为在 Bearer 之后拼接 Token  
示例：`Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b9836F45E23A345`

## 框架

1. [Django 中文文档](https://docs.djangoproject.com/zh-hans/4.2/)
2. [Django REST framework 中文文档](https://q1mi.github.io/Django-REST-framework-documentation/)
3. [Django-Rest-Knox](https://james1345.github.io/django-rest-knox/)

## 常用命令

```shell
pipreqs ./ --encoding=utf

# 镜像安装某个包
pip install Pillow --index-url=https://mirrors.aliyun.com/pypi/simple/

# 依赖管理
pip freeze > requirements.txt
pip install --index-url=https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 数据库
python manage.py makemigrations
python manage.py migrate

# 创建
django-admin startproject xxx
python manage.py startapp xxx
python manage.py createsuperuser

# 启动
python manage.py runserver
```


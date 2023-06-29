# django_base 说明

## 相关依赖

1. [Django 中文文档](https://docs.djangoproject.com/zh-hans/4.2/)
2. [Django REST framework 中文文档](https://q1mi.github.io/Django-REST-framework-documentation/)
3. [Django-Rest-Knox](https://james1345.github.io/django-rest-knox/)
4. [django-filter](https://django-filter.readthedocs.io/en/main/guide/usage.html#the-filter)

## 常用命令

```shell
pipreqs ./ --encoding=utf

# 镜像安装某个包
pip install django-filters --index-url=https://mirrors.aliyun.com/pypi/simple/

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

## Token Authentication(令牌认证)

在 Header 添加参数 Authorization，其值为在 Bearer 之后拼接 Token  
示例：`Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b9836F45E23A345`

## 管理员-用户

默认密码：登入**账户**  
重置密码：重置为登入**账户**

## 自定义异常状态码

`4000` 数据格式错误,data中描述多个字段的错误，msg中取第一个错误

## 分页参数

`page_index`页数  
`page_size`数量(默认10，最大100)

# django_base 说明

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
```

## 日志模块

### API 日志

重写`drf_api_logger`

- 修改信息
  1. 删除了`drf_api_logger`的模板等非必须的功能
  2. 在模型中添加发起请求的用户 id
  3. 增加日志保存时间``(默认会自动清理 3 天前的日志)
  4. 增加获取 API 的接口(拥有**过滤**功能)

### 系统日志

1. 配置 django 的原生日志保存为文件
2. 增加获取 API 及输出日志(压缩文件)的接口
3. 增加日志保存时间``(默认会自动清理 3 天前的日志)

## 用户模块

### 部门

1. 为用户添加 1 对 1 的部门信息

### 用户

1. 账户使用手机号
2. 默认密码：登入**账户**
3. 重置密码：重置为登入**账户**

## 认证模块

### Token Authentication(令牌认证)

在 Header 添加参数 Authorization，其值为在 Bearer 之后拼接 Token  
示例：`Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b9836F45E23A345`

## 特殊响应 code

> 默认响应的 **code** 为**状态码**

1. `4000` 数据格式错误,data 中会包含描述多个字段的错误，msg 中只取第一个错误

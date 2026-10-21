# django_base

基于 Django 4.2 和 Django REST framework 的后端基础模板，面向前后端分离项目，提供用户认证、用户管理、统一接口响应、分页过滤、文件上传及接口日志等通用能力，方便在此基础上扩展业务 API。

## 功能概览

- **用户认证**：以手机号为登录账号，支持注册、登录、退出当前设备和退出全部设备；使用 Knox 管理 Token。
- **个人账户**：获取和修改个人资料、修改密码、上传头像文件；修改密码后清除该用户的全部 Token。
- **用户管理**：超级管理员可查询、新增和修改用户，批量启用/禁用账户，设置管理员标记并重置密码。
- **接口规范**：统一 JSON 响应及异常处理，支持分页、django-filter 过滤和请求限流。
- **开发封装**：按 action 配置权限与序列化器，封装通用 CRUD、批量删除、自定义保存及文件上传逻辑。
- **接口日志**：通过本地 `logger` 模块记录请求、响应、用户、客户端 IP、状态码和执行耗时，支持敏感字段遮蔽及后台队列批量入库。
- **接口文档**：通过 DRF/CoreAPI 提供 `/docs/` 文档页面。

当前仓库为后端代码，不包含前端界面。`system` 系统配置模块已有模型、迁移与接口代码，但尚未注册应用和挂载根路由；日志查询路由及 Django Admin 也未启用。

## 技术栈

以下版本来自仓库依赖文件：

| 组件 | 版本 | 用途 |
| --- | --- | --- |
| Django | 4.2.2 | Web 框架、ORM、迁移 |
| Django REST framework | 3.14.0 | REST API |
| django-rest-knox | 4.2.0 | Token 认证 |
| django-filter | 23.2 | 查询过滤 |
| django-cors-headers | 4.1.0 | 跨域配置 |
| mysqlclient | 2.2.0 | MySQL 驱动 |
| coreapi | 2.3.3 | 接口文档 |
| django-redis | 5.3.0 | 可选 Redis 缓存支持 |
| django-apscheduler | 0.6.2 | 可选定时任务支持 |

## 目录结构

```text
django_base/
├── manage.py                     # Django 命令入口
├── urls.py                       # 根路由
├── config/
│   ├── settings/
│   │   ├── base/                 # 默认、应用、DRF、日志配置
│   │   ├── dev.py                # 开发环境配置
│   │   ├── pro.py                # 生产环境配置
│   │   └── __init__.py           # 按 ENV 选择环境
│   ├── asgi.py
│   └── wsgi.py
├── user/                         # 用户模型、认证与管理接口
├── logger/                       # 日志中间件、队列写入及查询代码
├── system/                       # 系统配置模块（尚未启用）
├── utils/                        # 视图、序列化、权限、响应等公共封装
├── media/                        # 上传文件及默认资源
├── requirements-my.txt           # 主要依赖清单
├── requirements.txt              # 完整冻结依赖（UTF-16 编码）
└── LICENSE                       # Apache License 2.0
```

## 本地启动

### 1. 创建环境并安装依赖

使用 Python 3.10 或 3.11 创建虚拟环境。仓库未提供 Python 版本锁定文件。

```bash
python3 -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

`requirements.txt` 为 UTF-16 编码的完整依赖文件；`requirements-my.txt` 为主要依赖清单，可按需用于安装主要依赖。安装 `mysqlclient` 时，系统需具备相应的 MySQL 客户端开发库和编译环境。

### 2. 配置数据库

默认加载 `config/settings/dev.py`，使用本机 MySQL 的 `django_base` 数据库。先创建数据库，再将该文件中 `DATABASES` 的用户名、密码、主机及端口改为本机配置：

```sql
CREATE DATABASE django_base CHARACTER SET utf8mb4;
```

若只需使用 SQLite 本地体验，可将 `dev.py` 中的 `DATABASES` 替换为：

```python
from pathlib import Path

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path(__file__).resolve().parents[2] / 'db.sqlite3',
    }
}
```

Redis 缓存配置默认被注释，本地启动无需 Redis 服务。项目不会自动读取 `.env` 文件，配置需在 settings 中修改，或自行接入环境变量读取逻辑。

### 3. 初始化并运行

在项目根目录执行：

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py runserver
```

创建超级管理员时，以手机号作为登录账号。启动后可访问：

- 接口文档：`http://127.0.0.1:8000/docs/`
- 用户接口根路径：`http://127.0.0.1:8000/api/user/`

根路径 `/` 没有配置首页，`/admin/` 当前未开放。

## 环境与配置

配置按 `DefaultSettings → BaseSettings → DRFSettings → LoggerSetting → dev/pro` 的顺序导入，后加载的同名配置覆盖前面的值。

| 配置项 | 当前行为 |
| --- | --- |
| `ENV` | 未设置或为空时加载 `dev.py`；任意非空值均加载 `pro.py` |
| `DEBUG` | 开发环境为 `True`，生产环境为 `False` |
| `IF_PERMISSION` | 默认 `True`，控制 `CommonViewSet` 的权限检查 |
| `MEDIA_ROOT` / `MEDIA_URL` | 默认 `media` / `/media/` |
| `TIME_ZONE` / `USE_TZ` | `Asia/Shanghai` / `False` |
| Token 请求头 | `Authorization: Bearer <token>` |
| Token 有效期 | 30 天，自动续期，最小刷新间隔 60 秒 |
| Token 数量 | 每个用户最多 10 个；达到上限时删除较早到期的 Token |
| 请求限流 | 匿名请求 30 次/分钟，已认证用户 60 次/分钟 |

切换生产配置，例如执行配置检查：

```bash
# macOS / Linux
ENV=production python manage.py check
```

```powershell
# Windows PowerShell
$env:ENV = 'production'
python manage.py check
```

`pro.py` 的 MySQL 配置目前被注释，因此生产环境沿用 `DefaultSettings.py` 中的 SQLite，实际路径为 `config/settings/db.sqlite3`。正式部署前应显式配置数据库、独立的 `SECRET_KEY`、允许的域名和跨域来源，并结合部署方式检查 CSRF 配置。当前配置允许所有主机及跨域来源，CSRF 中间件被注释，不能直接作为完整生产部署配置。

项目提供 `config.wsgi:application` 和 `config.asgi:application` 入口；生产服务需另行安装和配置相应服务器。上传目录应从项目根目录启动时使用，并由 Web 服务器或存储服务托管；开发服务器的媒体文件路由仅在 `DEBUG=True` 时生效。

## 常用接口

下表路径均包含完整前缀，默认使用末尾斜杠。

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/api/user/auth/login/` | 手机号、密码登录 | 公开 |
| POST | `/api/user/auth/logout/` | 退出当前 Token | 已登录 |
| POST | `/api/user/auth/logoutall/` | 退出全部 Token | 已登录 |
| POST | `/api/user/user/register/` | 注册账户 | 公开 |
| GET | `/api/user/user/me/` | 获取当前用户信息 | 已登录 |
| PUT | `/api/user/user/update_profile/` | 修改个人资料 | 已登录 |
| POST | `/api/user/user/set_password/` | 修改密码 | 已登录 |
| POST | `/api/user/user/upload/` | 上传头像文件 | 已登录 |
| GET | `/api/user/admin/user/` | 分页查询用户 | 超级管理员 |
| GET | `/api/user/admin/user/{id}/` | 查询用户详情 | 超级管理员 |
| POST | `/api/user/admin/user/save/` | 无 id 新增，有 id 更新 | 超级管理员 |
| PUT | `/api/user/admin/user/{id}/reset_password/` | 重置密码并清除全部 Token | 超级管理员 |
| PUT | `/api/user/admin/user/disable/` | 批量禁用，提交 `ids` 数组 | 超级管理员 |
| PUT | `/api/user/admin/user/enable/` | 批量启用，提交 `ids` 数组 | 超级管理员 |
| PUT | `/api/user/admin/user/{id}/active/` | 设置 `is_active` | 超级管理员 |
| PUT | `/api/user/admin/user/{id}/is_staff/` | 设置 `is_staff` | 超级管理员 |
| PUT | `/api/user/admin/user/{id}/is_superuser/` | 设置 `is_superuser` | 超级管理员 |

管理员新增用户及重置密码时，密码默认设为登录账号（手机号）。用户管理接口的访问条件是 `is_superuser`，仅有 `is_staff` 标记不满足条件。

### 调用示例

```bash
# 登录：从响应 data.token 中取得 Token
curl -X POST http://127.0.0.1:8000/api/user/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"phone":"13800138000","password":"<你的密码>"}'

# 获取个人信息
curl http://127.0.0.1:8000/api/user/user/me/ \
  -H 'Authorization: Bearer <token>'

# 修改密码；成功后需要重新登录
curl -X POST http://127.0.0.1:8000/api/user/user/set_password/ \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"old_password":"<旧密码>","new_password1":"<新密码>","new_password2":"<新密码>"}'

# 上传文件，使用 multipart/form-data，字段名为 file
curl -X POST http://127.0.0.1:8000/api/user/user/upload/ \
  -H 'Authorization: Bearer <token>' \
  -F 'file=@./avatar.png'
```

头像上传支持 `jpeg`、`gif`、`jpg`、`png` 扩展名，返回 `data.url`。上传动作只保存文件并返回地址，需要再调用资料修改接口，将地址写入 `avatar` 字段。

## 响应、分页与过滤

业务 JSON 接口统一包装为：

```json
{
  "data": {},
  "code": 0,
  "msg": "suc"
}
```

成功时 `code` 为 `0`；DRF 校验异常的业务码为 `4000`，其他已处理异常通常使用对应 HTTP 状态码。HTTP 状态码仍独立返回，例如注册成功为 `201`，退出登录为 `200`。开发模式下，未处理的系统异常会直接抛出供调试。

列表分页使用 `pageIndex` 和 `pageSize`，默认每页 10 条，最多 100 条。分页内容位于外层 `data` 中，包含 `count`、`next`、`previous`、`results`。

```text
GET /api/user/admin/user/?pageIndex=1&pageSize=20&username=张&real_name=张
```

`username` 和 `real_name` 支持模糊查询。过滤器中还保留了 `department_name` 配置，但当前用户模型没有 `department` 字段，使用该参数前需补齐模型关系或移除此过滤项。

## 扩展开发

- `utils/viewsets.py`：`CommonViewSet` 支持通过 `classes_map` 按 action 设置权限和序列化器，`response_page()` 简化分页返回。
- `CommonViewSetModel`：组合标准 CRUD、批量删除 `POST delete/` 和保存 `POST save/`；保存时有 `id` 则更新，无 `id` 则新增。
- `UploadFile`：可配置上传目录、文件扩展名、文件命名方式及用户唯一文件名。
- `utils/model_serializer.py`：`CommonSerializer` 提供基础字段选择及字段排除封装。
- `utils/renderer.py` / `utils/exception_handler.py`：集中维护响应格式和异常处理。
- `utils/permissions.py`：提供超级管理员权限类，并导出 DRF 标准权限类。

新增业务应用后，需注册 `INSTALLED_APPS`、挂载根路由，并生成和执行数据库迁移。启用 `system` 模块也需要完成这些步骤。

## 日志配置

日志配置集中于 `config/settings/base/LoggerSetting.py`，默认启用数据库记录和信号发送，可调整跳过的路由、命名空间以及敏感字段列表。

当前需注意以下实现细节：

- 日志查询路由在根 `urls.py` 中被注释。查询和清理任务位于 `logger/views.py`，不会随默认路由加载。
- 日志清理代码依赖 `django_apscheduler`，该应用目前未注册；启用前需注册应用、迁移任务表，并规划调度器启动方式，避免多进程重复调度。
- 配置文件中的刷新间隔名为 `DRF_LOGGER_QUEUE_FLUSH_INTERVAL`，写入线程实际读取 `DRF_LOGGER_INTERVAL`，未设置后者时默认每 10 秒刷新。
- 默认敏感字段列表未覆盖 `old_password`、`new_password1`、`new_password2`；开发模式的中间件还会打印原始请求体。处理真实数据前需完善日志脱敏与调试输出。

## 常用命令

```bash
# 检查配置
python manage.py check

# 生成和应用迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 执行测试（现有 tests.py 主要为默认占位文件）
python manage.py test

# 创建业务应用
python manage.py startapp your_app

# 监听局域网地址
python manage.py runserver 0.0.0.0:8000
```

## 许可证

本项目使用 [Apache License 2.0](LICENSE)。

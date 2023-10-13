from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

"""
配置表
"""
class SystemConfig(models.Model):
    # 配置项(枚举）
    CONFIG_TYPE = (
        ("USER_VERSION_NUM", '用户端版本号'),
        ("STAFF_VERSION_NUM", '员工端版本号'),
        ("ADMIN_VERSION_NUM", '管理员端版本号'),
        ("LOGO", 'logo'),
        ("USER_AGREEMENT", '用户协议'),
        ("PRIVACY_POLICY", '隐私政策'),
        ("SERVICE_MONITORING_AGREEMENT", '服务监督协议'),
    )
    config_name = models.CharField(max_length=64,choices=CONFIG_TYPE, verbose_name='配置名称')
    config_value = models.CharField(max_length=64, verbose_name='配置值')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_use = models.BooleanField(default=True, verbose_name='是否启用')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="操作用户", help_text="操作用户")
    class Meta:
        db_table = "system_config"
        verbose_name = "系统配置"
        verbose_name_plural = verbose_name
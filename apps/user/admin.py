from django.contrib import admin

from .models import User

# Register your models here.


@admin.register(User)
class UserManagerAdmin(admin.ModelAdmin):
    # 列表显示的字段
    list_display = ("name", "phone", "status", "create_time")
    # 列表筛选
    list_filter = ("status",)
    # 搜索框查询
    search_fields = ("name", "phone")
    search_help_text = "可输入 name, phone查询（支持模糊查询）"

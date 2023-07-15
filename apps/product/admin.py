from django.contrib import admin
from django.utils.html import format_html
from jsoneditor.forms import JSONEditor

# Register your models here.
from .models import *


@admin.register(Category)
class CategoryManagerAdmin(admin.ModelAdmin):
    list_display = ("name", "sort", "create_time")


# 内联模型 - 嵌套用
class Flavor(admin.StackedInline):
    model = DishFlavor
    extra = 1
    # json字段默认展示的是文本框，这里使用对应插件展示成json
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditor},
    }
    verbose_name_plural = "菜品口味"


@admin.register(Dish)
class DishManagerAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "show_img", "price", "status", "create_time")

    search_fields = ("name",)
    search_help_text = "输入菜品名称进行搜索"

    list_filter = ("category", "status")
    # 嵌套子模型 口味， 在添加商品时直接就把口味一起加了
    inlines = [Flavor]

    # 增加一个字段
    def show_img(self, obj):
        """

        :param obj: obj 为 一个Dish 的实例对象
        :return:
        """
        if obj.image:
            # obj.image.url 获取从midia的路径 /media/product/Snipaste_2023-07-12_20-31-22.png
            return format_html('<img src="{}" height="50"/>'.format(obj.image.url))
        else:
            return ""

    # 字段列表表头显示
    show_img.short_description = "图片"

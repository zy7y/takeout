from django.contrib import admin

from .models import *

# Register your models here.


@admin.register(Orders)
class OrderManagerAdmin(admin.ModelAdmin):
    list_display = ("number", "status", "user", "address_book", "phone", "amount")
    list_filter = ("status", "user")
    # 页面可编辑
    list_editable = ("status",)

    def phone(self, obj):
        if obj.address_book:
            return obj.address_book.phone

    phone.short_description = "联系电话"


@admin.register(OrderDetail)
class OrderManagerAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "dish",
        "dish_flavor",
        "number",
        "amount",
        "user",
        "address",
        "total",
    )
    search_fields = ("dish",)

    def user(self, obj):
        if obj.order and obj.order.user:
            return obj.order.user

    user.short_description = "用户"

    def address(self, obj):
        if obj.order and obj.order.address_book:
            return obj.order.address_book

    address.short_description = "收货地址"

    def total(self, obj):
        return obj.number * obj.amount

    total.short_description = "总价"

    list_filter = ("order", "order__user")

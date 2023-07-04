from django.db import models

from apps.product.models import Dish
from apps.user.models import AddressBook, User

# Create your models here.


class Orders(models.Model):
    number = models.CharField(max_length=50, blank=True, null=True, db_comment="订单号")
    status = models.IntegerField(
        db_comment="订单状态 1待付款，2待派送，3已派送，4已完成，5已取消", verbose_name="订单状态"
    )
    user = models.ForeignKey(
        User,
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        db_comment="下单用户",
        verbose_name="用户",
    )
    address_book = models.ForeignKey(
        AddressBook,
        null=True,
        db_constraint=False,
        on_delete=models.SET_NULL,
        db_comment="地址id",
        verbose_name="地址",
    )
    order_time = models.DateTimeField(db_comment="下单时间", verbose_name="下单时间")
    checkout_time = models.DateTimeField(db_comment="结账时间", verbose_name="结账时间")
    pay_method = models.IntegerField(
        db_comment="支付方式 1微信,2支付宝", default=1, verbose_name="支付方式"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, db_comment="实收金额", verbose_name="实收金额"
    )
    remark = models.CharField(
        max_length=100, blank=True, null=True, db_comment="备注", verbose_name="备注"
    )

    def __str__(self):
        return self.number

    class Meta:
        db_table = "orders"
        db_table_comment = "订单表"

        verbose_name = "订单"
        verbose_name_plural = "订单管理"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Orders,
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
        db_comment="订单id",
        verbose_name="订单",
    )
    dish = models.ForeignKey(
        Dish,
        db_constraint=False,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_comment="菜品id",
        verbose_name="菜品",
    )
    dish_flavor = models.CharField(
        max_length=50, blank=True, null=True, db_comment="口味", verbose_name="口味"
    )
    number = models.IntegerField(db_comment="数量", verbose_name="数量")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, db_comment="金额", verbose_name="金额"
    )

    def __str__(self):
        if self.order:
            return self.order.number

    class Meta:
        # managed = False
        db_table = "order_detail"
        db_table_comment = "订单明细表"

        verbose_name = "订单明细"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, db_constraint=False, null=True, on_delete=models.SET_NULL, db_comment="用户"
    )
    dish = models.ForeignKey(
        Dish,
        db_constraint=False,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_comment="菜品",
    )
    dish_flavor = models.CharField(
        max_length=50, blank=True, null=True, db_comment="口味"
    )
    number = models.IntegerField(db_comment="数量")
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_comment="金额")
    create_time = models.DateTimeField(
        blank=True, null=True, db_comment="创建时间", auto_now_add=True
    )

    class Meta:
        # 购物车我们不需要后台管理
        # managed = False
        db_table = "shopping_cart"
        db_table_comment = "购物车"

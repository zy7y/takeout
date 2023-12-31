# Generated by Django 4.2.2 on 2023-07-04 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0001_initial"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        db_comment="主键", primary_key=True, serialize=False
                    ),
                ),
                (
                    "dish_flavor",
                    models.CharField(
                        blank=True, db_comment="口味", max_length=50, null=True
                    ),
                ),
                ("number", models.IntegerField(db_comment="数量")),
                (
                    "amount",
                    models.DecimalField(
                        db_comment="金额", decimal_places=2, max_digits=10
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, db_comment="创建时间", null=True
                    ),
                ),
                (
                    "dish",
                    models.ForeignKey(
                        blank=True,
                        db_comment="菜品",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="product.dish",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_comment="用户",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="user.user",
                    ),
                ),
            ],
            options={
                "db_table": "shopping_cart",
                "db_table_comment": "购物车",
            },
        ),
        migrations.CreateModel(
            name="Orders",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        db_comment="主键", primary_key=True, serialize=False
                    ),
                ),
                (
                    "number",
                    models.CharField(
                        blank=True, db_comment="订单号", max_length=50, null=True
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        db_comment="订单状态 1待付款，2待派送，3已派送，4已完成，5已取消", verbose_name="订单状态"
                    ),
                ),
                (
                    "order_time",
                    models.DateTimeField(db_comment="下单时间", verbose_name="下单时间"),
                ),
                (
                    "checkout_time",
                    models.DateTimeField(db_comment="结账时间", verbose_name="结账时间"),
                ),
                (
                    "pay_method",
                    models.IntegerField(
                        db_comment="支付方式 1微信,2支付宝", default=1, verbose_name="支付方式"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        db_comment="实收金额",
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="实收金额",
                    ),
                ),
                (
                    "remark",
                    models.CharField(
                        blank=True,
                        db_comment="备注",
                        max_length=100,
                        null=True,
                        verbose_name="备注",
                    ),
                ),
                (
                    "address_book",
                    models.ForeignKey(
                        db_comment="地址id",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="user.addressbook",
                        verbose_name="地址",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_comment="下单用户",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="user.user",
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单",
                "verbose_name_plural": "订单管理",
                "db_table": "orders",
                "db_table_comment": "订单表",
            },
        ),
        migrations.CreateModel(
            name="OrderDetail",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        db_comment="主键", primary_key=True, serialize=False
                    ),
                ),
                (
                    "dish_flavor",
                    models.CharField(
                        blank=True,
                        db_comment="口味",
                        max_length=50,
                        null=True,
                        verbose_name="口味",
                    ),
                ),
                ("number", models.IntegerField(db_comment="数量", verbose_name="数量")),
                (
                    "amount",
                    models.DecimalField(
                        db_comment="金额",
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="金额",
                    ),
                ),
                (
                    "dish",
                    models.ForeignKey(
                        blank=True,
                        db_comment="菜品id",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="product.dish",
                        verbose_name="菜品",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        db_comment="订单id",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="order.orders",
                        verbose_name="订单",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单明细",
                "db_table": "order_detail",
                "db_table_comment": "订单明细表",
            },
        ),
    ]

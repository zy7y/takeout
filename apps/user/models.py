from django.db import models

# Create your models here.


class User(models.Model):
    # 不定义主键默认会给一个自增长的 id
    name = models.CharField(
        max_length=50, blank=True, null=True, db_comment="姓名", verbose_name="姓名"
    )
    phone = models.CharField(max_length=100, db_comment="手机号", verbose_name="手机号")
    status = models.IntegerField(
        blank=True, null=True, db_comment="状态 0:禁用，1:正常", verbose_name="状态"
    )
    create_time = models.DateTimeField(db_comment="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(
        db_comment="更新时间", auto_now=True, verbose_name="更新时间"
    )

    def __str__(self):
        return self.phone

    class Meta:
        # managed = False
        # 数据库的表名
        db_table = "user"
        # 数据库表备注
        db_table_comment = "用户信息"
        # verbose_name django admin 显示的
        verbose_name = "用户"
        verbose_name_plural = "用户管理"


class AddressBook(models.Model):
    # 数据库层面没绑定物理关系，字段是可空的外键字段，它允许引用的 User 对象不存在，并且在关联的 User 对象被删除时，user_id 字段的值将被设置为 NULL。
    # 数据库寸的字端其实就是user_id， user表的主键
    user = models.ForeignKey(
        User,
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="用户",
    )
    # user_id = models.BigIntegerField(db_comment='用户id')
    consignee = models.CharField(max_length=50, db_comment="收货人", verbose_name="收货人")
    sex = models.IntegerField(db_comment="性别 0 女 1 男", verbose_name="性别")
    phone = models.CharField(max_length=11, db_comment="手机号", verbose_name="手机号")
    province_code = models.CharField(
        max_length=12, blank=True, null=True, db_comment="省级区划编号"
    )
    province_name = models.CharField(
        max_length=32, blank=True, null=True, db_comment="省级名称"
    )
    city_code = models.CharField(
        max_length=12, blank=True, null=True, db_comment="市级区划编号"
    )
    city_name = models.CharField(
        max_length=32, blank=True, null=True, db_comment="市级名称"
    )
    district_code = models.CharField(
        max_length=12, blank=True, null=True, db_comment="区级区划编号"
    )
    district_name = models.CharField(
        max_length=32, blank=True, null=True, db_comment="区级名称"
    )
    detail = models.CharField(
        max_length=200, blank=True, null=True, db_comment="详细地址", verbose_name="详细地址"
    )
    label = models.CharField(
        max_length=100, blank=True, null=True, db_comment="标签", verbose_name="标签"
    )
    is_default = models.IntegerField(
        db_comment="默认 0 否 1是", default=0, verbose_name="是否默认"
    )
    create_time = models.DateTimeField(db_comment="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(
        db_comment="更新时间", auto_now=True, verbose_name="更新时间"
    )

    def __str__(self):
        return self.detail

    class Meta:
        # 为False Django 不管理表他的迁移、创建；实际工作中用到的多；我们需要创建表所以注释即可
        # managed = False
        db_table = "address_book"
        db_table_comment = "地址管理"
        verbose_name = "地址"
        verbose_name_plural = "地址管理"

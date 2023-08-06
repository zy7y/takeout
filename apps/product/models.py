from django.db import models

# Create your models here.


class Category(models.Model):
    TYPE = ((1, "菜品分类"), (2, "套餐分类"))
    # 套餐相关我们不做所以默认1就行了
    type = models.IntegerField(
        choices=TYPE, blank=True, null=True, db_comment="类型   1 菜品分类 2 套餐分类", default=1
    )
    name = models.CharField(
        unique=True, max_length=64, db_comment="分类名称", verbose_name="分类名称"
    )
    sort = models.IntegerField(db_comment="顺序", verbose_name="顺序")
    create_time = models.DateTimeField(db_comment="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(
        db_comment="更新时间", auto_now=True, verbose_name="更新时间"
    )

    def __str__(self):
        return self.name

    class Meta:
        # managed = False
        db_table = "category"
        db_table_comment = "菜品及套餐分类"

        verbose_name = "菜品分类"
        verbose_name_plural = "菜品分类管理"


class Dish(models.Model):
    STATUS = ((0, "停售"), (1, "启售"))
    name = models.CharField(
        unique=True, max_length=64, db_comment="菜品名称", verbose_name="菜品名称"
    )
    # 1个分类有多个商品
    category = models.ForeignKey(
        Category,
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="菜品分类",
    )
    # category_id = models.BigIntegerField(db_comment='菜品分类id')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_comment="菜品价格",
        verbose_name="菜品价格",
    )
    code = models.CharField(max_length=64, db_comment="商品码", verbose_name="商品码")
    image = models.ImageField(upload_to="product/", verbose_name="图片", db_comment="图片")
    description = models.CharField(
        max_length=400, blank=True, null=True, db_comment="描述信息"
    )
    status = models.IntegerField(
        choices=STATUS, default=1, db_comment="0 停售 1 起售", verbose_name="售卖状态"
    )
    sort = models.IntegerField(db_comment="顺序", verbose_name="顺序")
    sale = models.IntegerField(db_comment="销量", verbose_name="销量", default=0)
    create_time = models.DateTimeField(db_comment="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(
        db_comment="更新时间", auto_now=True, verbose_name="更新时间"
    )

    def __str__(self):
        return self.name

    class Meta:
        # managed = False
        db_table = "dish"
        db_table_comment = "菜品管理"

        verbose_name = "菜品"
        verbose_name_plural = "菜品管理"


class DishFlavor(models.Model):
    dish = models.ForeignKey(
        Dish,
        db_constraint=False,
        on_delete=models.SET_NULL,
        null=True,
        db_comment="菜品",
        verbose_name="菜品",
    )
    name = models.CharField(max_length=64, db_comment="口味名称", verbose_name="口味名称")
    value = models.JSONField(
        blank=True, null=True, db_comment="口味数据list", verbose_name="口味详情"
    )
    create_time = models.DateTimeField(db_comment="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(
        db_comment="更新时间", auto_now=True, verbose_name="更新时间"
    )

    def __str__(self):
        return self.name

    class Meta:
        # managed = False
        db_table = "dish_flavor"
        db_table_comment = "菜品口味关系表"

        verbose_name = "口味"
        verbose_name_plural = "口味管理"

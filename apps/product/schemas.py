import json
from typing import Optional, List

from ninja import ModelSchema, Schema, Field

from pydantic import validator

from .models import Category, Dish, DishFlavor
from ..order.models import ShoppingCart


class CategorySchema(ModelSchema):
    class Config:
        model = Category
        model_fields = "__all__"


class DishFilter(Schema):
    status: Optional[int] = Field(..., description="上架状态")
    category_id: Optional[int] = Field(..., description="分类ID", alias="categoryId")


class DishFlavorSchema(ModelSchema):
    value: List[str]

    # 处理value 是json 数组的情况 最终返回的数据
    @validator("value")
    def dumps_value(cls, value):
        if value:
            # 源版中 value 返回的是dumps之后的数组数据
            return json.dumps(value)

    class Config:
        model = DishFlavor
        # model_exclude = ["dish"]
        model_fields = "__all__"


class DishSchema(ModelSchema):
    flavors: List[DishFlavorSchema] = []
    saleNum: int = Field(..., alias="sale")

    class Config:
        model = Dish
        model_fields = "__all__"


class ShoppingCartSchema(ModelSchema):
    image: Optional[str] = None
    name: Optional[str] = None
    dishId: Optional[int] = None

    @validator('dishId', always=True)
    def compute_dish_id(cls, v, values):
        return values['dish']

    class Config:
        model = ShoppingCart
        model_fields = "__all__"


class AddCartSchema(ModelSchema):
    dish_id: int = Field(..., alias="dishId", description="食品ID")
    dish_flavor: str = Field("", alias="dishFlavor", description="口味")

    class Config:
        model = ShoppingCart
        model_exclude = ['id', 'create_time', 'number', 'user']


class SubCartSchema(Schema):
    dish_id: int = Field(..., alias="dishId", description="食品ID")

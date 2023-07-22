import logging
from datetime import datetime
from typing import List, Any

from ninja import Schema, Field, ModelSchema

from apps.order.models import Orders, OrderDetail
from pydantic import validator


class OrderSubmitSchema(Schema):
    remark: str
    pay_method: int = Field(..., description="支付方式", alias="payMethod")
    address_book_id: int = Field(..., description="地址ID", alias="addressBookId")


class OrderDetailSchema(ModelSchema):
    name: str = Field(None, description="商品名称")

    class Config:
        model = OrderDetail
        model_fields = "__all__"


class OrderSchema(ModelSchema):
    orderDetails: List[OrderDetailSchema] = []
    orderTime: Any = Field(None, alias="order_time")

    @validator("orderTime")
    def fmt_order_time(cls, value, values):
        if value is not None:
            return values["order_time"].strftime('%Y-%m-%d %H:%M:%S')  # 格式化日期时间字符串

    class Config:
        model = Orders
        model_fields = "__all__"


class OrdersResponse(Schema):
    total: int
    page_number: int
    page_size: int
    pages: int
    records: List[OrderSchema]

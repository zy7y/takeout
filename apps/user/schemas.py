from ninja import Schema, Field, ModelSchema

from .models import AddressBook


class SendMsgSchema(Schema):
    phone: str = Field(..., description="手机号", regex=r'^1[3456789]\d{9}$')


class SendMsgResultSchema(Schema):
    code: str = Field(..., description="验证码")


class UserLoginSchema(SendMsgSchema, SendMsgResultSchema):
    pass


class AddressBookSchema(ModelSchema):
    # 兼容H5
    sex: str
    isDefault: int = Field(..., alias="is_default")

    class Config:
        model = AddressBook
        model_fields = "__all__"


class AddressBookCreateSchema(ModelSchema):
    """
    {
    "consignee": "渣渣辉",
    "phone": "18716356843",
    "sex": "1",
    "detail": "福建省厦门市集美区厦门市图书馆集美分馆2号门",
    "label": "学校"
}
    """

    class Config:
        model = AddressBook
        model_fields = ['consignee', 'phone', 'sex', 'detail', 'label']


class AddressBookSetDefaultSchema(Schema):
    id: int

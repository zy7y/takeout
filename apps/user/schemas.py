from ninja import Schema, Field


class SendMsgSchema(Schema):
    phone: str = Field(..., description="手机号", regex=r'^1[3456789]\d{9}$')


class SendMsgResultSchema(Schema):
    code: str = Field(..., description="验证码")


class UserLoginSchema(SendMsgSchema, SendMsgResultSchema):
    pass

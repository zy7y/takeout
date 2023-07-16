import random

from django.shortcuts import render

# Create your views here.

from ninja import Router

from .models import User
from .schemas import SendMsgSchema, SendMsgResultSchema, UserLoginSchema
from ..schemas import R

router = Router(tags=['登录'])


@router.post("/sendMsg", summary="验证码", response=R[SendMsgResultSchema])
def send_msg(request, data: SendMsgSchema):
    # 4位数，生成验证码
    code = ''.join(random.choices('0123456789', k=4))
    # 验证码存在session中
    request.session[data.phone] = code
    request.session.set_expiry(5*60)  # 缓存5分钟
    # 使用了response R， 这里默认就是 R 中的 data属性
    return R.ok(data=SendMsgResultSchema(code=code))


@router.post("/login", summary="登录", response=R)
def user_login(request, data: UserLoginSchema):
    # 1. 验证码存在?
    if request.session.get(data.phone) == data.code:
        # 2. 查不到就创建
        user, _ = User.objects.get_or_create(phone=data.phone, status=1)
        # 3. Java原版这里使用的是存session 为了偷懒-不改动h5 我们也不用JWT了
        request.session['user'] = user.id
        return R.ok(data=None)
    return R.fail("验证码错误")


@router.post("/loginout", summary="退出", response=R)
def user_logout(request):
    if request.session.get("user"):
        request.session.delete("user")
    return R.ok(data=None)
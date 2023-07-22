from typing import List

from ninja import Router

from apps.auth import auth
from apps.schemas import R
from apps.user.models import AddressBook
from apps.user.schemas import AddressBookSchema, AddressBookCreateSchema, AddressBookSetDefaultSchema

router = Router(tags=["地址"], **auth)


@router.get("/default", summary="获取默认地址", response=R[AddressBookSchema])
def get_user_default_address(request):
    try:
        obj = AddressBook.objects.get(user_id=request.session["user"], is_default=1)
        return R.ok(data=obj)
    except AddressBook.DoesNotExist:
        return R.fail()


@router.post("", summary="新增收货地址", response=R)
def addr_default(request, data: AddressBookCreateSchema):
    AddressBook.objects.create(**data.dict(), user_id=request.session["user"])
    return R.ok(None)


@router.get("/list", summary="收货地址列表", response=R[List[AddressBookSchema]])
def addr_list(request):
    objs = AddressBook.objects.filter(user_id=request.session["user"]).order_by('-is_default', '-create_time')
    return R.ok([obj for obj in objs])


@router.put("/default", summary="设置默认地址", response=R[AddressBookSchema])
def set_addr_default(request, data: AddressBookSetDefaultSchema):
    user_id = request.session["user"]
    try:
        obj = AddressBook.objects.get(id=data.id)
        # 该用户已有的默认地址去除
        AddressBook.objects.filter(user_id=user_id, is_default=1).update(is_default=0)
        # 设置默认地址
        obj.is_default = 1
        obj.save()
        return R.ok(data=obj)
    except AddressBook.DoesNotExist:
        return R.fail()


@router.get("/{pk}", summary="获取地址详情", response=R[AddressBookSchema])
def detail(request, pk: int):
    try:
        obj = AddressBook.objects.get(id=pk)
        return R.ok(data=obj)
    except AddressBook.DoesNotExist:
        return R.fail()


@router.put("", summary="更新地址信息", response=R)
def update(request, data: AddressBookSchema):
    AddressBook.objects.filter(id=data.id).update(**data.dict(exclude={'id', 'user', 'isDefault'}))
    return R.ok()


@router.delete("", summary="删除地址信息", response=R)
def delete(request, ids: int):
    try:
        obj = AddressBook.objects.get(id=ids)
        obj.delete()
        return R.ok()
    except AddressBook.DoesNotExist:
        return R.fail()

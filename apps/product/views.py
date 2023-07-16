import os.path
from typing import List

from django.http import FileResponse
from django.shortcuts import render

# Create your views here.

from ninja import Router, Query

from apps.order.models import ShoppingCart
from apps.product.models import Category, Dish
from apps.product.schemas import CategorySchema, DishSchema, DishFilter, ShoppingCartSchema, AddCartSchema, \
    SubCartSchema
from apps.schemas import R

from takeout.settings import BASE_DIR

router = Router(tags=["商品"])


@router.get("/category/list", summary="分类", response=R[List[CategorySchema]])
def category_list(request):
    result = Category.objects.all().order_by('-sort')
    return R.ok(data=list(result))


@router.get("/dish/list", summary="食品列表", response=R[List[DishSchema]])
def dish_list(request, data: DishFilter = Query(...)):
    result = Dish.objects.filter(**data.dict())
    # 将口味属性加到对象中
    for obj in result:
        setattr(obj, "flavors", obj.dishflavor_set.all())
    return R.ok(list(result))


@router.get("/shoppingCart/list", tags=["购物车"], summary="购物车列表", response=R[List[ShoppingCartSchema]])
def cart(request):
    if request.session.get("user"):
        result = ShoppingCart.objects.filter(user=request.session["user"])
        for obj in result:
            setattr(obj, "image", obj.dish.image)
            setattr(obj, "name", obj.dish.name)
        return R.ok(data=list(result))
    return R.ok(data=[])


@router.get("/common/download", summary="图片")
def download_img(request, name: str):
    media_path = f"{BASE_DIR}{name}"
    if os.path.exists(media_path):
        return FileResponse(open(media_path, "rb"), content_type="image/png")


from ..auth import  auth


@router.post("/shoppingCart/add", summary="添加购物车", tags=["购物车"], **auth,
             response=R[ShoppingCartSchema])
def cart_add(request, data: AddCartSchema):
    user = request.session["user"]
    try:
        obj = ShoppingCart.objects.get(user_id=user, dish_id=data.dish_id)
        obj.number += 1
        obj.save()
    except ShoppingCart.DoesNotExist:
        obj = ShoppingCart.objects.create(
            user_id=user,
            number=1,
            **data.dict()
        )

    return R.ok(obj)


@router.post("/shoppingCart/sub", summary="修改购物车", tags=["购物车"], **auth,
             response=R[ShoppingCartSchema])
def cart_sub(request, data: SubCartSchema):
    try:
        user = request.session["user"]
        obj = ShoppingCart.objects.get(dish_id=data.dish_id, user_id=user)
        if obj.number - 1 <= 0:
            obj.delete()
        else:
            obj.number -= 1
            obj.save()
        return R.ok(obj)
    except ShoppingCart.DoesNotExist:
        return R.fail("对象不存在")


@router.delete("/shoppingCart/clean", summary="清空购物车", tags=["购物车"], **auth,
               response=R)
def cart_clean(request):
    ShoppingCart.objects.filter(user_id=request.session["user"]).delete()
    return R.ok()

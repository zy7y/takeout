import os.path
from typing import List

from django.http import FileResponse
from django.shortcuts import render

# Create your views here.

from ninja import Router, Query

from apps.order.models import ShoppingCart
from apps.product.models import Category, Dish
from apps.product.schemas import CategorySchema, DishSchema, DishFilter, ShoppingCartSchema
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
    if request.session.get('user'):
        result = ShoppingCart.objects.filter(user=request.session.get("user"))
        return R.ok(data=list(result))
    return R.ok(data=[])


@router.get("/common/download", summary="图片")
def download_img(request, name: str):
    media_path = f"{BASE_DIR}{name}"
    if os.path.exists(media_path):
        return FileResponse(open(media_path, "rb"), content_type="image/png")

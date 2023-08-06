import uuid

from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum, F

# Create your views here.
from ninja import Router, Query

from apps.auth import auth
from apps.order.models import ShoppingCart, Orders, OrderDetail
from apps.order.schemas import OrderSubmitSchema, OrdersResponse
from apps.schemas import R
from apps.user.models import AddressBook

router = Router(tags=["订单"], **auth)


@router.post("/submit", summary="提交订单", response=R)
def submit(request, data: OrderSubmitSchema):
    user_id = request.session["user"]

    # 1. 检查收货地址是否存在
    if not AddressBook.objects.filter(id=data.address_book_id, user_id=user_id).exists():
        return R.fail("收货地址不存在")

    # 2. 查购物车
    carts = ShoppingCart.objects.filter(user_id=user_id)
    if not carts.exists():
        return R.fail("无商品数据")

    # 3. 计算订单总价
    # SELECT SUM("number" * "amount") AS "total_amount" FROM "shopping_cart"
    amount = carts.aggregate(total_amount=Sum(F('number') * F('amount')))['total_amount']

    # 在事务中创建订单和订单详情
    with transaction.atomic():
        # 创建订单
        order_obj = Orders.objects.create(
            number=str(uuid.uuid4()),
            user_id=user_id,
            amount=amount,
            status=2,
            order_time=timezone.now(),
            checkout_time=timezone.now(),
            **data.dict()
        )
        # 批量创建订单详情（子订单）
        order_details = []
        for entry in carts:
            order_details.append(OrderDetail(
                order=order_obj,
                dish=entry.dish,
                dish_flavor=entry.dish_flavor,
                number=entry.number,
                amount=entry.amount
            ))
            entry.dish.sale += entry.number
            entry.dish.save()
        OrderDetail.objects.bulk_create(order_details)

        # 清空购物车
        carts.delete()

    return R.ok(None)


@router.get("/userPage", summary="订单列表", response=R[OrdersResponse])
def user_order_list(request, page: int, page_size: int = Query(..., alias="pageSize")):
    query_sets = Orders.objects.filter(user_id=request.session["user"]).order_by('-order_time')

    # 创建 Paginator 对象并传入 QuerySet 和每页记录数量
    paginator = Paginator(query_sets, page_size)

    try:
        # 获取指定页码的 Page 对象
        orders_page = paginator.page(page)
        for order in orders_page:
            details = order.orderdetail_set.all()
            for detail in details:
                setattr(detail, "name", detail.dish.name)
            setattr(order, "orderDetails", details)

        # 将 Page 对象转换为字典格式
        orders_dict = {
            'total': orders_page.paginator.count,
            'page_number': orders_page.number,
            'pages': paginator.num_pages,  # 添加最大页数
            'page_size': page_size,
            'records': list(orders_page)
        }

        return R.ok(data=OrdersResponse(**orders_dict))
    except EmptyPage:
        # 处理页码超出范围的情况
        return R.ok(data=[])


@router.post("/again", summary="再来一单")
def again(request):
    return R.ok()
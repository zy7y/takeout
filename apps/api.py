from ninja import NinjaAPI
from ninja.errors import AuthenticationError
from ninja.responses import JsonResponse

from apps.user.views import router as user_router
from apps.product.views import router as product_router

app = NinjaAPI(title="DjangoNinja-瑞吉外卖H5", description="使用DjangoNinja实现《瑞吉外卖》项目")

app.add_router("/user", router=user_router)
app.add_router("", router=product_router)


@app.exception_handler(AuthenticationError)
def handle_auth_error(request, exc):
    # H5 跳转到登录页
    return JsonResponse(dict(msg="NOTLOGIN", code=0, data=None)
                        )


@app.get("/index")
def index(request):
    return "Hello Django Ninja"

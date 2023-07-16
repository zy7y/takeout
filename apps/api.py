from ninja import NinjaAPI

from apps.user.views import router as user_router

app = NinjaAPI(title="DjangoNinja-瑞吉外卖H5", description="使用DjangoNinja实现《瑞吉外卖》项目")

app.add_router("/user", router=user_router)

@app.get("/index")
def index(request):
    return "Hello Django Ninja"

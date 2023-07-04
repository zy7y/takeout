from ninja import NinjaAPI

app = NinjaAPI(title="DjangoNinja-瑞吉外卖H5", description="使用DjangoNinja实现《瑞吉外卖》项目")


@app.get("/index")
def index(request):
    return "Hello Django Ninja"

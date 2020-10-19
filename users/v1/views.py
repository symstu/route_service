async def authenticate(request):
    return JSONResponse()


async def login(request):
    return JSONResponse()


async def register(request):
    return JSONResponse()


routes = [
    Route('/auth/', endpoint=authenticate),
    Route('/login/', endpoint=login),
    Route('/register/', endpoint=register)
]

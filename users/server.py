from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route



app = Starlette(routes=routes)

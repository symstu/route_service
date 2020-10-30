from starlette.applications import Starlette

from v1.views import routes


app = Starlette(routes=routes)

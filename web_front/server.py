import uvicorn

from starlette.applications import Starlette

from components.auth import views as auth_views
from components.routes import views as routes_views

from config import conf


routes = auth_views.routes + routes_views.routes
app = Starlette(routes=routes)


if __name__ == '__main__':
    uvicorn.run('server:app', port=conf.server_port, reload=True)

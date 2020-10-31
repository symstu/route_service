import uvicorn

from starlette.applications import Starlette

from components.auth import views
from config import conf


app = Starlette(routes=views.routes)


if __name__ == '__main__':
    uvicorn.run('server:app', port=conf.server_port, reload=True)

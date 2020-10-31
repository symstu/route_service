import uvicorn

from starlette.applications import Starlette

from v1.views import routes
from config import conf


app = Starlette(routes=routes)


if __name__ == '__main__':
    uvicorn.run('server:app', port=conf.server_port, reload=True)

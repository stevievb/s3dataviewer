import logging
import sys

from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec,
)

# from s3ImageCloud.db import close_pg, init_pg
# from s3ImageCloud.middlewares import setup_middlewares
from s3DataViewer.routes import setup_routes
from s3DataViewer.settings import get_config


def init_app(argv=None):
    app = web.Application()

    app['config'] = get_config(argv)

    # setup views and routes
    setup_routes(app)

    # setup_middlewares(app)

    # init docs with all parameters, usual for ApiSpec
    setup_aiohttp_apispec(
        app=app,
        title="s3DataViewer API Documentation",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )

    return app


def main(argv):
    logging.basicConfig(level=logging.ERROR)

    app = init_app(argv)

    config = get_config(argv)

    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])

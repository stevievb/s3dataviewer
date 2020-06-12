import logging
import sys

from bokeh.server.server import Server
from .apps.image import bokeh_image_app

def main(argv):
    logging.basicConfig(level=logging.ERROR)

    server = Server(
        {'/image': bokeh_image_app},  # list of Bokeh applications
        allow_websocket_origin=['*'],
        host='http://localhost:4200'
    )

    # start timers and services and immediately return
    server.run_until_shutdown()


if __name__ == '__main__':
    main(sys.argv[1:])

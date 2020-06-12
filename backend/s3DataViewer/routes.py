import aiohttp_cors

from .views import ping, get_plots, build_index


def setup_cors(app):
    return aiohttp_cors.setup(app, defaults={
        # Allow all to read all CORS-enabled resources from
        # http://client.example.org.
        "*": aiohttp_cors.ResourceOptions(allow_methods='*', expose_headers="*",
                allow_headers="*")
    })


def setup_routes(app):
    cors = setup_cors(app)

    ping_resource = cors.add(app.router.add_resource('/ping'))
    cors.add(ping_resource.add_route("GET", ping))

    plots_resource = cors.add(app.router.add_resource('/plots'))
    cors.add(plots_resource.add_route("GET", get_plots))

    index_resource = cors.add(app.router.add_resource('/index'))
    cors.add(index_resource.add_route("PUT", build_index))

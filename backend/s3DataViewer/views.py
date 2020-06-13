from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema
)
from aiohttp import web
import pandas as pd
import re
from bokeh.embed import server_document, server_session
from bokeh.client import pull_session
from bokeh.util.session_id import generate_session_id
from bokeh.util.token import generate_jwt_token
import os

from .utils import get_matching_s3_keys
from .models import PlotsRequestSchema, S3ObjectBokehPlotSchema, IndexRequestSchema, S3ObjectRecordSchema, \
    S3ObjectBokehPlotsGetResponseSchema


@docs(
    tags=["status"],
    summary="Get a status of HTTP 200 OK if server is up",
    description="An endpoint to test the server status",
)
async def ping(request):
    return web.HTTPOk()


@docs(
    tags=["image"],
    summary="Get a list of bokeh plots",
    description="Returns a list of bokeh html tags to embed in a webpage",
)
@request_schema(PlotsRequestSchema, location='query')
@response_schema(S3ObjectBokehPlotsGetResponseSchema())
async def get_plots(request):
    loaded_request = PlotsRequestSchema().load(request.query)
    offset = loaded_request['offset']
    limit = loaded_request['limit']
    total_length = len(request.app['keys_df'].index)
    selected_keys = request.app['keys_df'].sort_values(loaded_request['sort'],
                                                       ascending=loaded_request['ascending']).iloc[
                    offset:limit + offset]
    record_dicts_list = selected_keys.to_dict(orient='records')
    for i, record in enumerate(record_dicts_list):
        localhost_url = 'http://' + os.environ['SERVER_HOST_NAME'] + ':5006/image'

        arguments = {'key': record['Key'], 'bucket': request.app['bucket'],
                     'width': loaded_request['width'],
                     'height': loaded_request['height']}

        resources = 'default' if i == 0 else None
        record['bokeh_tag'] = server_document(localhost_url,
                                              arguments=arguments)

        record['script_src'] = re.search(', "(.*)", true', record['bokeh_tag']).group(1)
        record['script_id'] = re.search('id="(.*)"', record['bokeh_tag']).group(1)
        record['session_id'] = generate_session_id()  # session.id
        record['token'] = generate_jwt_token(record['session_id'])
    response_data = S3ObjectBokehPlotsGetResponseSchema().dump({'plots': record_dicts_list, 'length': total_length})
    return web.json_response(response_data)


@docs(
    tags=["index"],
    summary="Build the index",
    description="Rebuilds the searchable, paginatable, index of objects in S3 bucket given bucket and prefix",
)
@request_schema(IndexRequestSchema, location='body')
async def build_index(request):
    body = await request.read()
    loaded_request = IndexRequestSchema().loads(body)
    keys = get_matching_s3_keys(bucket=loaded_request['bucket'], prefix=loaded_request['prefix'])
    request.app['keys_df'] = pd.DataFrame.from_records(keys)
    request.app['bucket'] = loaded_request['bucket']
    return web.HTTPOk()

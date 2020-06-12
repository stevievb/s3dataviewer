from bokeh.application.handlers import FunctionHandler, DirectoryHandler
from bokeh.application import Application

import numpy as np
import holoviews as hv
import boto3
from PIL import Image
import holoviews.plotting.bokeh  # important
from bokeh.io import show, curdoc
from bokeh.layouts import layout
import io
from holoviews.operation.datashader import datashade
from bokeh.models import Slider, Button

from marshmallow import Schema, fields, INCLUDE

renderer = hv.renderer('bokeh').instance(mode='server')


class BokehImageAppArgsSchema(Schema):
    bucket = fields.List(fields.String())
    key = fields.List(fields.String())
    height = fields.List(fields.Integer())
    width = fields.List(fields.Integer())


# Define valid function for FunctionHandler
# when deploying as script, simply attach to curdoc
def modify_doc(doc):
    args = doc.session_context.request.arguments

    args_schema = BokehImageAppArgsSchema()
    loaded_args = args_schema.load(args, unknown=INCLUDE)

    bucket = loaded_args['bucket'][0]
    key = loaded_args['key'][0]

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)

    file_stream = io.BytesIO()
    object.download_fileobj(file_stream)
    pil_image = Image.open(file_stream)

    hv_img_plot = hv.Image(np.asarray(pil_image)).options(
        height=loaded_args['height'][0], width=loaded_args['width'][0])
    # Create HoloViews plot and attach the document
    hvplot = renderer.get_plot(hv_img_plot, doc)

    # Combine the holoviews plot and widgets in a layout
    plot = layout([
        [hvplot.state]], sizing_mode='fixed')

    doc.add_root(plot)
    return doc


bokeh_image_app = Application(FunctionHandler(modify_doc))

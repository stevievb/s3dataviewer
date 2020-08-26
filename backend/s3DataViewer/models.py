from marshmallow import Schema, fields


class PlotsRequestSchema(Schema):
    filter_regex = fields.Str(description="A regex to filter keys")
    sort = fields.Str(missing='Key')
    ascending = fields.Boolean(missing=True, default=True)
    limit = fields.Integer(missing=20, default=20)
    offset = fields.Integer(missing=0, default=0)
    height = fields.Integer(missing=200)
    width = fields.Integer(missing=200)


class IndexRequestSchema(Schema):
    bucket = fields.Str(description="name of S3 bucket containing data to be rendered", required=True)
    prefix = fields.Str(description="Limits the response to keys that begin with the specified prefix", missing="")
    suffix = fields.Str(missing="")   


class S3ObjectRecordSchema(Schema):
    ETag = fields.String()
    Key = fields.String()
    LastModified = fields.DateTime()
    Size = fields.Integer()
    StorageClass = fields.String()


class S3ObjectBokehPlotSchema(S3ObjectRecordSchema):
    bokeh_tag = fields.String()
    script_src = fields.String()
    script_id = fields.Integer()
    session_id = fields.String()
    token = fields.String()


class S3ObjectBokehPlotsGetResponseSchema(Schema):
    plots = fields.Nested(S3ObjectBokehPlotSchema, many=True)
    length = fields.Integer()

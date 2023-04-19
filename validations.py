from marshmallow import Schema, fields, post_load, validate
from webargs import fields


class TaskSchema(Schema):
    name = fields.Str(required=True)
    min = fields.Float(required=True)
    likely = fields.Float(required=True)
    max = fields.Float(required=True)


tasks_schema = TaskSchema(many=True)
task_schema = TaskSchema()


class ImageOptSchema(Schema):
    width = fields.Integer(missing=16)
    height = fields.Integer(missing=9)
    bins = fields.Integer(missing=20)
    density = fields.Boolean(missing=True)
    alpha = fields.Float(missing=0.75)
    label = fields.Str(missing="Teste")
    xlabel = fields.Str(missing="eixo X")
    ylabel = fields.Str(missing="eixo Y")
    title = fields.Str(missing="Estimativa")


class ImageSchema(Schema):
    plot = fields.Boolean(required=True)
    img_opt = fields.Nested(ImageOptSchema, missing=None)

    @post_load
    def set_default_img_opt(self, data, **kwargs):
        if data["plot"] and data["img_opt"] is None:
            data["img_opt"] = ImageOptSchema().load({})
        return data


class PostRequestSchema(Schema):
    tasks = fields.Field(
        required=True,
        error_messages={
            "required": "O campo 'tasks' é obrigatório e deve ser enviado."
        }
    )
    iterations = fields.Integer(missing=1000)
    type = fields.Str(
        validate=validate.OneOf(["triangular", "normal"]),
        missing="triangular"
    )
    percentiles = fields.Field(missing=[50, 80, 90, 100])
    image = fields.Nested(ImageSchema, required=True)


class PutRequestSchema(Schema):
    tasks = fields.Field(
        required=True,
        error_messages={
            "required": "O campo 'tasks' é obrigatório e deve ser enviado."
        }
    )
    iterations = fields.Integer(missing=1000)
    type = fields.Str(
        validate=validate.OneOf(["triangular", "normal"]),
        missing="triangular"
    )
    percentiles = fields.Field(missing=[50, 80, 90, 100])
    image = fields.Nested(ImageSchema, required=False)


post_request_schema = PostRequestSchema()
put_request_schema = PutRequestSchema()

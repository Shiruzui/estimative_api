from marshmallow import Schema, post_load
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


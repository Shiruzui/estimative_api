from marshmallow import Schema, post_load
from webargs import fields


class TaskSchema(Schema):
    class Meta:
        ordered = True
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
    label = fields.Str(missing="Histograma")
    xlabel = fields.Str(missing="Tempo (dias)")
    ylabel = fields.Str(missing="Frequência")
    title = fields.Str(missing="Distribuição de tempo das tarefas")


class ImageSchema(Schema):
    plot = fields.Boolean(required=True)
    img_opt = fields.Nested(ImageOptSchema, missing=None)

    @post_load
    def set_default_img_opt(self, data, **kwargs):
        if data["plot"] and data["img_opt"] is None:
            data["img_opt"] = ImageOptSchema().load({})
        return data

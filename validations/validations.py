from marshmallow import Schema, post_load, validate, validates_schema
from webargs import fields
from exceptions.color_value_error import ColorValueError
from exceptions.task_value_error import TaskValueError
from matplotlib.colors import is_color_like

def validate_color(value):
    if not is_color_like(value):
        raise ColorValueError("O valor fornecido não é uma cor válida.")


def validate_min_likely_max(min_value, likely_value, max_value):
    if min_value > likely_value or likely_value > max_value:
        raise TaskValueError("Os valores devem seguir a ordem: 'min' <= 'likely' <= 'max'")

class TaskSchema(Schema):
    class Meta:
        ordered = True
    # TODO: definir valor mínimo e se deve ser 'float' ou 'int'
    name = fields.Str(required=True)
    min = fields.Float(required=True, validate=validate.Range(min=1))
    likely = fields.Float(required=True, validate=validate.Range(min=1))
    max = fields.Float(required=True, validate=validate.Range(min=1))

    @validates_schema
    def check_min_likely_max(self, data, **kwargs):
        min_value = data.get('min')
        likely_value = data.get('likely')
        max_value = data.get('max')
        validate_min_likely_max(min_value, likely_value, max_value)


class ImageOptSchema(Schema):
    width = fields.Integer(missing=16)
    height = fields.Integer(missing=9)
    bins = fields.Integer(missing=20)
    density = fields.Boolean(missing=True)
    alpha = fields.Float(missing=0.75)
    label = fields.Str(missing="Histograma")
    xlabel = fields.Str(missing="Tempo (dias)")
    # ylabel = fields.Str(missing="Frequência")
    title = fields.Str(missing="Distribuição de tempo das tarefas")
    dist_color = fields.Str(missing="blue", validate=validate_color)
    mean_color = fields.Str(missing="red", validate=validate_color)
    median_color = fields.Str(missing="lime", validate=validate_color)
    grid = fields.Bool(missing=True)
    font_size = fields.Integer(missing=8, validate=validate.Range(min=12, max=30))


class ImageSchema(Schema):
    plot = fields.Boolean(required=True)
    img_opt = fields.Nested(ImageOptSchema, missing=None)

    @post_load
    def set_default_img_opt(self, data, **kwargs):
        if data["plot"] and data["img_opt"] is None:
            data["img_opt"] = ImageOptSchema().load({})
        return data

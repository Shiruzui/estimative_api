from marshmallow import Schema, validate
from webargs import fields
from validations.validations import ImageSchema


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


post_request_schema = PostRequestSchema()
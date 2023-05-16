from marshmallow import Schema, validate
from webargs import fields
from validations.validations import ImageSchema, TaskSchema


class PostRequestSchema(Schema):
    tasks = fields.Nested(
        TaskSchema,
        many=True,
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            "required": "O campo 'tasks' é obrigatório e deve ser enviado.",
            "empty": "A lista de tarefas não pode ser vazia."
        }
    )
    iterations = fields.Integer(missing=1000)
    type = fields.Str(
        validate=validate.OneOf(["triangular", "normal"]),
        missing="triangular"
    )
    percentiles = fields.List(fields.Integer(), missing=[50, 80, 90, 100])
    image = fields.Nested(ImageSchema, required=True)
    participants = fields.Integer(
        validate=validate.Range(min=1),
        error_messages={
            "required": "O campo 'participants' é obrigatório e deve ser enviado.",
            "invalid": "O campo 'participants' deve ser um número inteiro maior ou igual a 1."
        }
    )


post_request_schema = PostRequestSchema()

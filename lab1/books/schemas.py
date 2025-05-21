from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    title = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100, error="The name must be between 2 and 100 characters."),
        ]
    )
    author = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=50, error="Author name must be between 2 and 50 characters long"),
        ]
    )
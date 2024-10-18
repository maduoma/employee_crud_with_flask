from marshmallow import Schema, fields, validate, ValidationError

def validate_profile_picture(value):
    if value and not value.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError("Profile picture must be a .png, .jpg, or .jpeg file.")

class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=[validate.Length(min=1, max=100)])
    email = fields.Email(required=True, validate=[validate.Length(max=120)])
    position = fields.Str(required=True, validate=[validate.Length(min=1, max=100)])
    salary = fields.Float(required=True, validate=[validate.Range(min=0)])
    date_hired = fields.DateTime(dump_only=True)
    profile_picture = fields.Str(validate=[validate.Length(max=200), validate_profile_picture])

# Instantiate schema for validation and serialization
employee_schema = EmployeeSchema()
employee_list_schema = EmployeeSchema(many=True)

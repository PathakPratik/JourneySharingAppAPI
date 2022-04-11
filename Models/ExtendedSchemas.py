from marshmallow import Schema, fields, ValidationError

class MatchUsersSchema(Schema):
    UserId = fields.Integer(required=False)
    TripStartLocation = fields.List(fields.String(), required=True)
    TripStopLocation = fields.List(fields.String(), required=True)
    time = fields.Float(required=False)
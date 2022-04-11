from marshmallow import Schema, fields, ValidationError

class MatchUsersSchema(Schema):
    UserId = fields.Integer(required=False)
    TripStartLocation = fields.List(fields.String(), required=True)
    TripStopLocation = fields.List(fields.String(), required=True)
    time = fields.String(required=False)
    ScheduleTime = fields.String(required=False)
    GenderPrefrence = fields.String(required=False)
    RequiredRating = fields.String(required=False)
    ModeOfTransport = fields.String(required=False)
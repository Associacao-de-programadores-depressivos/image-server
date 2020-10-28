from tortoise.models import Model
from tortoise import fields


class FirebaseToken(Model):
    device_id = fields.CharField(max_length=255, pk=True)
    token = fields.CharField(max_length=255, null=False)
    created_date = fields.DatetimeField(auto_now=True)
import json
from datetime import datetime

def fix(field) -> None:
    if isinstance(field, datetime):
        return field.isoformat()

def dumps(value: dict):
    return json.dumps(value, default=fix)

import re
from fastapi import HTTPException

OBJECT_ID_REGEX = re.compile(r'^[0-9a-fA-F]{24}$')

def validate_object_id(object_id: str):
    if not OBJECT_ID_REGEX.match(object_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
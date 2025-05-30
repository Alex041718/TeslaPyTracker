from bson import ObjectId, json_util
import json
from datetime import datetime
import re

def is_valid_object_id(id_str):
    """Vérifie si une chaîne est un ObjectId MongoDB valide"""
    return ObjectId.is_valid(id_str)

def parse_json(data):
    """Convertit les types BSON en JSON"""
    return json.loads(json_util.dumps(data))

def format_datetime(dt):
    """Formate un objet datetime"""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return None

def validate_email(email):
    """Valide un format d'email"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
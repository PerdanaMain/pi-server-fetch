from flask import request, jsonify
from datetime import datetime, timezone
import pytz
import random

def get_values(web_id):
  random_value = random.uniform(0, 400)
  random_int = random.randint(0, 9)
  
  timestamp = f"2024-09-13T0{random_int}:0{random_int}:00Z"
  utc_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
  gmt_plus_7 = pytz.timezone('Asia/Jakarta') 
  local_time = utc_time.astimezone(gmt_plus_7)
  formatted_local_time = local_time.isoformat(timespec='seconds')
  
  
  data = {
    "Timestamp": formatted_local_time,
    "Values": random_value,
    "UnitsAbbreviation": "",
    "Good": True,
    "Questionable": False,
    "Substituted": False,
    "Annotations": False
  }
  
  return jsonify({"message": "Hello, World!", "data":data}), 200
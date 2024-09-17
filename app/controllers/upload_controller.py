from flask import request, jsonify
from config import Config
import pandas as pd
import psycopg2
import uuid 

def upload():
  try:
    if 'file' not in request.files:
      return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
      return jsonify({"message": "No selected file"}), 400
    
    df = pd.read_excel(file)

    arr = [tuple(x) for x in df.to_numpy()]
    arr = [x[:1] + x[2:14] + x[23:] for x in arr]
    
    
    conn = psycopg2.connect(
      host=Config.HOST,
      database=Config.DATABASE,
      user=Config.USER,
      password=Config.PASSWORD,
    )
    id = uuid.uuid4()
    
    
    curr = conn.cursor()
    
    query = "INSERT INTO master_tag (web_id, name, path, descriptor, point_class, point_type, digital_set_name, engineering_units, span, zero, step, future,display_digits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    curr.executemany(query, arr)
    
    conn.commit()
    curr.close()
    conn.close()
    
    return jsonify({"status": "success", "message": "Data inserted successfully", "data":arr}), 200
  except Exception as e:
    print(e)
    return jsonify({"message": str(e)}), 500
  
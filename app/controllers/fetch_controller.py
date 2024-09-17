from flask import request, jsonify, make_response
from datetime import datetime, timezone
from app.models.master_tag import MasterTag
from app.models.value_tag import ValueTag
from requests.auth import HTTPBasicAuth
from app import db
import os
import requests
import threading
import time
import asyncio
import aiohttp
import json
from requests.exceptions import ConnectionError, Timeout, RequestException


def check_connection():
    host = os.getenv("PI_SERVER_ENDPOINT")
    msg = "Checking connection to the server..."
    try:
        test_conn = requests.get(
            host, 
            auth=HTTPBasicAuth(username=os.getenv("PI_SERVER_USERNAME"), password=os.getenv("PI_SERVER_PASSWORD")),
            verify=False,  # Avoid SSL verification for this example
            timeout=10  # Set a timeout for the request
        )
        # Check for successful response (status code 200)
        if test_conn.status_code == 200:
            print("Connection successful, status code:", test_conn.status_code)
            return True
        else:
            print(f"Received unexpected status code: {test_conn.status_code}")
            return False

    except ConnectionError:
        print("Error: Unable to connect to the server. The connection was lost.")
        return False
    except Timeout:
        print("Error: The request timed out.")
        return False
        
    except RequestException as e:
        print(f"An error occurred: {e}")
        return False
        

def index():
  conn = check_connection()
  
  if conn == False:
    return make_response(jsonify({"message": "Failed to connect to the server"}), 500)
  
  while True:
    master_tags = MasterTag.query.with_entities(MasterTag.id, MasterTag.web_id).all()
    tags = [{"id":mt.id,'web_id': mt.web_id} for mt in master_tags]
    
    host = os.getenv("PI_SERVER_ENDPOINT")
    base_url = host+"streams/{}/value"
    urls = [base_url.format(tag['web_id']) for tag in tags]
    
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start fetching data")
    asyncio.run(send_data(urls,tags))
  

def save_data(data, tags):
  try:
    # Save data to the database
    for i in range(len(data)):
      tag = tags[i]
      values = data[i]
      
      if "Value" not in values:
        continue
      
      value = values['Value']
      if isinstance(value, dict):
        value = value["Value"]
        
      elif not isinstance(value, (str, float, int, bool)):
        value = str(value)
      
      new_value = ValueTag(
        tag_id=tag['id'],
        time_stamp=values['Timestamp'],
        value=value,
        units_abbreviation=values["UnitsAbbreviation"],
        good=values["Good"],
        questionable=values["Questionable"],
        substituted=values["Substituted"],
        annotated=values["Annotated"]
      )
      
      db.session.add(new_value)
      
    db.session.commit()
    return make_response(jsonify({"message": "Data berhasil disimpan"}), 200)
      
  except Exception as e:
    print("An error occurred: ", str(e))


async def send_data(urls,tags):
  try:
    async with aiohttp.ClientSession() as session:
      for i in range(0,len(urls), len(urls)):
        batch_urls = urls[i:i + len(urls)]
        
        tasks = [fetch_data(session, url) for url in batch_urls]
        res = await asyncio.gather(*tasks)
        
        save_data(res, tags)
        
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Data has been saved")
        await asyncio.sleep(60)
        continue
  except Exception as e:
    print('An exception occurred : ', str(e))
    

async def fetch_data(session, url):
  # Fetch data from a single URL asynchronously
  username = os.getenv("PI_SERVER_USERNAME")
  password = os.getenv("PI_SERVER_PASSWORD")

  try:
    auth = aiohttp.BasicAuth(login=username, password=password)
    async with session.get(url, auth=auth, ssl=False) as response:
      response.raise_for_status()
      data = await response.json() 
      return data  
  except Exception as e:
    return {"error": f"An error occurred: {str(e)}"}
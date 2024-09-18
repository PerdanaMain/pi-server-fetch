from app import app
from flask import make_response, jsonify
from app.controllers import upload_controller, value_controller,fetch_controller
from config import Config
import os

@app.route('/')
def index():
    return make_response(jsonify({"message": "API Works!"}), 200)

@app.route("/fetch", methods=["POST"])
def fetch():
    return fetch_controller.index()

@app.route("/test", methods=["GET"])
def test():
    try:
        return make_response(jsonify({"message": "Fetching data successfully",}), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}), 500)

@app.route("/stream/<web_id>/values", methods=["GET"])
def show_values(web_id):
    return value_controller.get_values(web_id)

@app.route("/upload", methods=["POST"])
def store():
    return upload_controller.upload()
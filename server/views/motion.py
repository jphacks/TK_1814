from flask import Blueprint, jsonify, request
import requests
from database import session
from model import User, Promise
import os
import uuid
from datetime import datetime as DT


app = Blueprint('motion_bp', __name__)


@app.route('/record', methods=['POST'])
def post():
    return jsonify({'results': 'OK'}), 200
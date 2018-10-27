from flask import Blueprint, jsonify, request
import requests
from database import session
from model import User, Promise
import os
import uuid
from goolabs import GoolabsAPI
from config import GOO_API_KEY, DOCOMO_API_KEY
from datetime import datetime as DT
from sqlalchemy import or_

app = Blueprint('promise_bp', __name__)

@app.route('/promise/<id>', methods=['GET'])
def get(id):
    # id    ユーザID

    promises = session.query(Promise, User).filter(
        or_(Promise.master_user_id == id, Promise.slave_user_id == id),
        or_(User.id == Promise.master_user_id, User.id == Promise.slave_user_id),
        User.id != id,
        Promise.is_done == False
    ).all()

    results = []
    for promise, user in promises:
        results.append({
            'created_at': promise.created_at.strftime('%Y年%m月%d日'),
            'limited_at': '' if promise.limit_date is None else promise.limit_date.strftime('%Y年%m月%d日'),
            'img': user.profile,
            'name': user.name,
            'content': promise.content,
            'is_master': True if str(promise.master_user_id) == str(id) else False,
        })

    return jsonify({'results': results})

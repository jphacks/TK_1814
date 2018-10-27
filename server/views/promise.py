from flask import Blueprint, jsonify
from database import session
from model import User, Promise
from sqlalchemy import or_

app = Blueprint('promise_bp', __name__)


@app.route('/promise/<user_id>', methods=['GET'])
def get(user_id):
    # user_id    ユーザID

    promises = session.query(Promise, User).filter(
        or_(Promise.master_user_id == user_id, Promise.slave_user_id == user_id),
        or_(User.id == Promise.master_user_id, User.id == Promise.slave_user_id),
        User.id != user_id,
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
            'is_master': True if str(promise.master_user_id) == str(user_id) else False,
        })

    return jsonify({'results': results})

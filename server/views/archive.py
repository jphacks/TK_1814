from flask import Blueprint, jsonify
from database import session
from model import User, Promise
from sqlalchemy import or_
from itertools import groupby
from config import HOST_TOP


app = Blueprint('archive_bp', __name__)


@app.route('/archive/<user_id>', methods=['GET'])
def get_(user_id):

    results = []

    promises = session.query(Promise, User).filter(
        or_(Promise.master_user_id == user_id, Promise.slave_user_id == user_id),
        or_(User.id == Promise.master_user_id, User.id == Promise.slave_user_id),
        Promise.is_done == True,
        User.id != user_id
    ).all()

    promises.sort(key=lambda tmp_promise: tmp_promise[1].id)
    for user_id, promise_list in groupby(promises, key=lambda tmp_promise: tmp_promise[1].id):

        user = [tmp_promise_user[1] for tmp_promise_user in promises if tmp_promise_user[1].id == user_id][0]

        results.append({
            'count': len(list(promise_list)),
            'img': '{}/{}'.format(HOST_TOP, user.profile),
            'name': user.name,
            'user_id': user.id
        })

    session.close()
    return jsonify({'results': results}), 200

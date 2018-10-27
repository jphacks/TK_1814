from flask import Blueprint, jsonify, request
from database import session
from model import User, Promise
from sqlalchemy import or_
from config import HOST_TOP


app = Blueprint('promise_bp', __name__)


@app.route('/promise/<user_id>', methods=['GET'])
def get(user_id):
    # user_id    ユーザID

    promises = session.query(Promise, User).filter(
        or_(Promise.master_user_id == user_id, Promise.slave_user_id == user_id),
        or_(User.id == Promise.master_user_id, User.id == Promise.slave_user_id),
        User.id != user_id,
        Promise.is_done == False
    ).order_by(Promise.created_at.desc()).all()

    results = []
    for promise, user in promises:
        results.append({
            'id': promise.id,
            'created_at': promise.created_at.strftime('%Y年%m月%d日'),
            'limited_at': '' if promise.limit_date is None else promise.limit_date.strftime('%Y年%m月%d日'),
            'calendar_date': '' if promise.limit_date is None else promise.limit_date.strftime('%Y/%m/%d %H:%M:%S'),
            'img': '{}/{}'.format(HOST_TOP, user.profile),
            'name': user.name,
            'content': promise.content,
            'is_master': True if str(promise.master_user_id) == str(user_id) else False,
            'one_side_done': None if promise.one_side_done_user_id is None else promise.one_side_done_user_id
        })

    session.close()

    return jsonify({'results': results})


@app.route('/promise', methods=['PUT'])
def put():
    # 受け取る値
    # user_id       userID -1ならNoneにして、達成を解除する。それ以外（正しいユーザID）なら普通にupdate
    # promise_id    promiseID

    promise = session.query(Promise).filter(Promise.id == request.json['promise_id']).one_or_none()

    if not (promise.master_user_id == request.json['user_id'] or promise.slave_user_id == request.json['user_id']):
        session.close()
        return jsonify({'results': '権限なし'}), 403


    if request.json['user_id'] == -1:
        promise.one_side_done_user_id = None

        session.commit()
        session.close()

        return jsonify({'results': '約束の承認を解除'}), 200


    if promise.one_side_done_user_id is None:
        promise.one_side_done_user_id = request.json['user_id']
        msg = '片方が承認しました'
    elif promise.one_side_done_user_id == request.json['user_id']:
        msg = '何もしないよ'
    else:
        promise.one_side_done_user_id = None
        promise.is_done = True
        msg = '約束の承認をお互いにしました'

    session.commit()
    session.close()

    return jsonify({'results': msg}), 200

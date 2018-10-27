from flask import Blueprint, jsonify, request
from database import session
from model import User, Promise, Motion
from datetime import datetime as DT

app = Blueprint('motion_bp', __name__)


@app.route('/motion', methods=['POST'])
def post():
    # user_id
    # promise_id -1ならNone
    # created_at 2012-12-29 13:49:37の形式

    user = session.query(User).filter(User.id == request.json['user_id']).one_or_none()
    promise = session.query(Promise).filter(Promise.id == request.json['promise_id']).one_or_none()

    motion = Motion()
    motion.user_id = user.id
    motion.promise_id = None if promise is  None else promise.id
    motion.created_at = DT.strptime(request.json['created_at'], '%Y-%m-%d %H:%M:%S')

    session.add(motion)
    session.commit()
    session.close()

    return jsonify({'results': 'OK'}), 200
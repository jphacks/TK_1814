from flask import Blueprint, jsonify, request
from database import session
from model import User, Promise
from sqlalchemy import or_


app = Blueprint('archive_bp', __name__)


@app.route('/archive/<user_id>', methods=['GET'])
def get_(user_id):

    # promise = session.query(Promise).filter()

    session.close()
    return jsonify({'results': user_id}), 200

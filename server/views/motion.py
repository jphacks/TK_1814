from flask import Blueprint, jsonify, request
from database import session
from model import User, Promise, Motion
import os
from datetime import datetime as DT
import datetime

app = Blueprint('motion_bp', __name__)


@app.route('/motion', methods=['POST'])
def post():

    # マッチング判定
    # モーションテーブルから近い時刻のレコードがあるか検索。
    # なかったら、モーションテーブルに時刻を追加。
    start = DT.now()

    print('******************:')
    print(start)
    print(start - datetime.timedelta(seconds=5))
    print('******************:')

    # motion = session.query(Motion).filter(Motion.created_at.between())

    ### 約束IDあり
    # あったら、そのレコードにあるユーザIDを持ってきて約束テーブルの該当レコードに追記。
    #
    # ### 約束IDなし
    # あったら、そのレコードにあるユーザIDと約束IDを持ってきて、約束テーブルの該当レコードに追記。


    return jsonify({'results': 'OK'}), 200
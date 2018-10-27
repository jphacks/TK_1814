from flask import Blueprint, jsonify, request
import requests
from database import session
from model import User, Promise
import os
import uuid
from goolabs import GoolabsAPI
from config import GOO_API_KEY, DOCOMO_API_KEY
from datetime import datetime as DT

app = Blueprint('record_bp', __name__)


def get_promise_content(text):
    api = GoolabsAPI(GOO_API_KEY)
    index = 0
    # letter = "明日の13時10分岩見と一緒に東京駅に来て"
    # 時刻情報正規化API
    # chrono_response = api.chrono(sentence=letter)
    # 固有表現抽出API
    entity_response = api.entity(sentence=text)
    # 形態素解析API
    # morph_response = api.morph(sentence=letter)

    print('*********************')
    print(entity_response['ne_list'])
    print('*********************')

    date = ''
    time = ''

    for i in range(len(entity_response["ne_list"])):

        # 日付の抽出
        if entity_response["ne_list"][i][1] == "DAT":
            day_response = api.chrono(sentence=entity_response["ne_list"][i][0])
            date = day_response["datetime_list"][i][1]

            # 約束内容の要素番号を算出
            day = entity_response["ne_list"][i][0]
            index = text.find(day) + len(day)

        # 時間の抽出
        elif entity_response["ne_list"][i][1] == "TIM":
            time = entity_response["ne_list"][i][0]

            # 約束内容の要素番号を算出
            time = entity_response["ne_list"][i][0]
            index = text.find(time) + len(time)

    morph_response = api.morph(sentence=text[index:len(text)])
    if morph_response["word_list"][0][0][1] == u"格助詞":
        content = text[index + 1:len(text)]
    else:
        content = text[index:len(text)]

    return {'date': date, 'time': time, 'content': content}


@app.route('/record', methods=['POST'])
def post():
    # wav   file
    # id    ユーザID

    from app import app
    wav = request.files['wav']
    _, file_ext = os.path.splitext(wav.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'sound', str(uuid.uuid4()) + file_ext)
    wav.save(path)

    # 音声　→　テキスト
    url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(DOCOMO_API_KEY)
    files = {"a": open(path, 'rb'), "v": "on"}
    r = requests.post(url, files=files)

    # テキスト　→　日付、時刻、内容に分割
    user = session.query(User).filter(User.id == request.form['id']).one_or_none()
    results = get_promise_content(r.json()['text'])
    # new_promise = Promise(
    #     master_user_id=user.id,
    #     limit_date= None if results['date'] == '' else DT.strptime('{} {}'.format(results['date'], results['time']), '%Y-%m-%d %H時%M分'),
    #     content=results['content']
    # )

    # master_user = db.relationship("User", foreign_keys=[master_user_id])
    # slave_user = db.relationship("User", foreign_keys=[slave_user_id])
    # content = db.Column(db.String(255), nullable=False)
    # limit_date

    return jsonify({'results': ''})

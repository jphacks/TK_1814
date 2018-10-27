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


def get_promise_content(letter):
    api = GoolabsAPI(GOO_API_KEY)
    index = 0
    # letter = "クリスマスに岩見と一緒に東京駅に来て"
    # 時刻情報正規化API
    # chrono_response = api.chrono(sentence=letter)
    # 固有表現抽出API
    entity_response = api.entity(sentence=letter)
    # 形態素解析API
    # morph_response = api.morph(sentence=letter)

    date = ''
    hour = ''
    min = ''
    place = ''

    for i in range(len(entity_response["ne_list"])):

        # 日付の抽出
        if entity_response["ne_list"][i][1] == "DAT":
            day_response = api.chrono(sentence=entity_response["ne_list"][i][0])

            if len(day_response['datetime_list']) != 0:
                date = day_response["datetime_list"][0][1]

                # 約束内容の要素番号を算出
                day = entity_response["ne_list"][i][0]
                index = letter.find(day) + len(day)

        # 時間の抽出
        elif entity_response["ne_list"][i][1] == "TIM":
            time_len = len(entity_response["ne_list"][i][0])

            for j in range(time_len):

                if entity_response["ne_list"][i][0][j] == u"時":
                    hour = entity_response["ne_list"][i][0][0:j]
                    hour_n = j

                    if j != time_len - 1:
                        if entity_response["ne_list"][i][0][j + 1] == u"半":
                            min = "30"

                elif entity_response["ne_list"][i][0][j] == u"分":
                    min = entity_response["ne_list"][i][0][hour_n + 1:j]

            # 約束内容の要素番号を算出
            time = entity_response["ne_list"][i][0]
            index = letter.find(time) + len(time)

        elif entity_response["ne_list"][i][1] == "LOC":
            place = entity_response["ne_list"][i][0]

    # 約束内容を出力
    # 約束内容の最初の文字に格助詞が入ってるか調べる
    morph_response = api.morph(sentence=letter[index:len(letter)])
    if morph_response["word_list"][0][0][1] == u"格助詞":
        par_len = len(morph_response["word_list"][0][0][0])

        content = letter[index + par_len:len(letter)]
    else:
        content = letter[index:len(letter)]

    return {'date': date, 'hour': hour, 'min': min, 'content': content, 'place': place}


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

    date = results['date']
    hour = '' if results['hour'] == '' else results['hour'].zfill(2)
    min = '' if results['min'] == '' else results['min'].zfill(2)

    if date == '' and hour == '':
        limit = None
    elif date != '' and hour == '':
        limit = DT.strptime('{}'.format(date), '%Y-%m-%d 09:00:00')
    elif date != '' and hour != '':
        limit = DT.strptime('{} {}:{}'.format(date, hour, min.zfill(2)), '%Y-%m-%d %H:%M')

    new_promise = Promise(
        master_user_id=user.id,
        limit_date= limit,
        content=results['content']
    )

    session.add(new_promise)
    session.commit()
    session.close()

    return jsonify({
        'promise': {
            'id': new_promise.id,
            'limit_date': '' if limit is None else str(new_promise.limit_date),
            'content': new_promise.content,
            'full_text': r.json()['text']
        },
        'results': results
    })

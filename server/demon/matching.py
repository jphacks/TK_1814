import sys
sys.path.append('/home/kenta/pinky')

from itertools import groupby
import time
from database import session
from model import User, Motion, Promise
import datetime


def sample():
    while True:
        filepath = '/home/kenta/pinky/demon/test.log'
        log_file = open(filepath,'a')
        try:
            log_file.write(time.ctime()+"\n")
        finally:
            log_file.close()
            time.sleep(3)


def sample2():
    all_motion = session.query(Motion).all()
    user_motion = {}
    delete_motion_list = []

    all_motion.sort(key=lambda tmp_motion: tmp_motion.user_id)
    for user_id, motions in groupby(all_motion, key=lambda tmp_motion: tmp_motion.user_id):
        tmp_motion_list = []

        for motion in motions:
            tmp_motion_list.append(motion)
            # delete_motion_list.append(motion)

        user_motion[user_id] = tmp_motion_list


    user_id_list = []

    print(user_motion)

    for user_id in user_motion:
        if len(user_motion[user_id]) >= 2:
            delete_motion_list += user_motion[user_id]
            user_id_list.append(user_id)

    print(user_id_list)
    print('HOGEHOGE: ', delete_motion_list)

    matching_results = []


    for i in range(len(user_id_list) - 1):
        firstA = user_motion[user_id_list[i]][0].created_at
        lastA = user_motion[user_id_list[i]][1].created_at

        for j in range(i + 1, len(user_id_list)):
            firstB = user_motion[user_id_list[j]][0].created_at
            lastB = user_motion[user_id_list[j]][1].created_at

            if abs(firstA - firstB).total_seconds() <= 5 and abs(lastA - lastB).total_seconds() <= 5:
                # マッチング結果

                if user_motion[user_id_list[i]][0].promise_id is None:
                    matching_results.append({'promise_id': user_motion[user_id_list[j]][0].promise_id, 'slave_user_id': user_id_list[i]})
                else:
                    matching_results.append({'promise_id': user_motion[user_id_list[i]][0].promise_id, 'slave_user_id': user_id_list[j]})

                print(user_id_list[i], user_id_list[j])


    print(matching_results)

    updates = []

    for result in matching_results:
        promise = session.query(Promise).filter(Promise.id == result['promise_id']).one_or_none()
        promise.slave_user_id = result['slave_user_id']

        updates.append(promise)

    session.bulk_save_objects(updates)

    for motion in delete_motion_list:
        session.delete(motion)

    session.commit()
    session.close()

if __name__ == '__main__':
    sample2()

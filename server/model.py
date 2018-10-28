from database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    profile = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '{}({})'.format(self.name, self.id)


class Promise(db.Model):
    __tablename__ = 'promise'

    id = db.Column(db.Integer, primary_key=True)
    master_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default=None)
    slave_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default=None)
    content = db.Column(db.String(255), nullable=False)
    limit_date = db.Column(db.DateTime, nullable=True, default=None)
    is_done = db.Column(db.Boolean, nullable=False, default=False) # 両方がDoneした時にTrue
    one_side_done_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default=None) # 2人が約束を承認・未承認ならNone、片方が承認しているならその人のIDが入る
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    master_user = db.relationship("User", foreign_keys=[master_user_id])
    slave_user = db.relationship("User", foreign_keys=[slave_user_id])
    one_side_done_user = db.relationship("User", foreign_keys=[one_side_done_user_id])

    def __repr__(self):
        return '{}({})'.format(self.content, self.id)


class Motion(db.Model):
    __tablename__ = 'motion'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    promise_id = db.Column(db.Integer, db.ForeignKey('promise.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user = db.relationship("User", foreign_keys=[user_id])
    promise = db.relationship("Promise", foreign_keys=[promise_id])

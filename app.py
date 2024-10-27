from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# SQLite 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Event 테이블 모델 정의
class Event(db.Model):  # 기존 SNS를 Event로 변경
    id = db.Column(db.Integer, primary_key=True)
    작성일 = db.Column(db.String, nullable=False)
    카테고리 = db.Column(db.String, nullable=False)
    지역 = db.Column(db.String, nullable=False)
    행사명 = db.Column(db.String, nullable=False)
    내용 = db.Column(db.String, nullable=False)
    장소 = db.Column(db.String, nullable=False)
    일시 = db.Column(db.String, nullable=True)
    대상 = db.Column(db.String, nullable=True)
    접수기간 = db.Column(db.String, nullable=True)
    문의 = db.Column(db.String, nullable=True)
    신청링크 = db.Column(db.String, nullable=True)
    게시물링크 = db.Column(db.String, nullable=True)
    페이지링크 = db.Column(db.String, nullable=True)

# 앱 실행 시 테이블이 없으면 생성되도록 설정
with app.app_context():
    db.create_all()  # 테이블이 없는 경우에만 생성

@app.route('/')
def index():
    events = Event.query.all()  # Event 테이블의 모든 데이터 조회
    return render_template('index.html', event_data=events)

if __name__ == "__main__":
    app.run(debug=True)

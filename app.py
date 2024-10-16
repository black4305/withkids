from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# SQLite 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sns.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SNS 테이블 모델 정의
class SNS(db.Model):
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

# JSON 파일을 읽고 DB에 데이터 삽입
def insert_data_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)['values']  # 'values' 항목에 데이터가 있음
        for row in data[1:]:  # 나머지 데이터 삽입
            sns = SNS(
                작성일=row[0],
                카테고리=row[1],
                지역=row[2],
                행사명=row[3],
                내용=row[4],
                장소=row[5],
                일시=row[6] if len(row) > 6 else None,
                대상=row[7] if len(row) > 7 else None,
                접수기간=row[8] if len(row) > 8 else None,
                문의=row[9] if len(row) > 9 else None,
                신청링크=row[10] if len(row) > 10 else None,
                게시물링크=row[11] if len(row) > 11 else None,
                페이지링크=row[12] if len(row) > 12 else None
            )
            db.session.add(sns)
        db.session.commit()

# 앱 컨텍스트 내에서 테이블을 생성하고 데이터 삽입
with app.app_context():
    db.create_all()  # 테이블 생성
    insert_data_from_json('sns_data.json')  # JSON 파일에서 데이터 삽입

@app.route('/')
def index():
    sns_data = SNS.query.all()  # DB에서 모든 SNS 데이터를 가져오기
    return render_template('index.html', sns_data=sns_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
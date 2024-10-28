from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# 데이터베이스 파일 경로 설정
EVENT_DB_PATH = os.path.join("data", "event.db")
NINO_TRIP_DB_PATH = os.path.join("data", "nino-trip.db")

# 데이터베이스 초기화 함수
def initialize_db():
    conn = sqlite3.connect(EVENT_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event (
            작성일 TEXT,
            카테고리 TEXT,
            지역 TEXT,
            행사명 TEXT,
            내용 TEXT,
            장소 TEXT,
            일시 TEXT,
            대상 TEXT,
            접수기간 TEXT,
            문의 TEXT,
            신청링크 TEXT,
            게시물링크 TEXT,
            페이지링크 TEXT
        )
    ''')
    conn.commit()
    conn.close()

# event.db에서 데이터 가져오기
def get_event_data():
    conn = sqlite3.connect(EVENT_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM event")
    columns = [description[0] for description in cursor.description]
    events = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return events

# nino-trip.db에서 데이터 가져오기
def get_nino_trip_data():
    conn = sqlite3.connect(NINO_TRIP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nino_trip")
    columns = [description[0] for description in cursor.description]
    nino_trip = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return nino_trip

@app.route('/')
def index():
    event_data = get_event_data()
    nino_trip_data = get_nino_trip_data()
    return render_template('index.html', event_data=event_data, nino_trip_data=nino_trip_data)

if __name__ == '__main__':
    initialize_db()  # 초기화 함수 호출
    app.run(debug=True)

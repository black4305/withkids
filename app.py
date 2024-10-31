from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# 데이터베이스 파일 경로 설정
EVENT_DB_PATH = os.path.join("data", "event.db")
NINO_TRIP_DB_PATH = os.path.join("data", "nino-trip.db")
FOREST_DB_PATH = os.path.join("data", "forest.db")
CAFE_DB_PATH = os.path.join("data", "cafe.db")

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
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT 지역, 장소, `알짜 팁`, 나이, 가격, `실내/실외`, 링크 FROM TravelData")
    data = cursor.fetchall()
    conn.close()
    
    # 데이터에서 '-'로 구분된 항목들을 \n으로 줄바꿈 처리하여 HTML로 전달
    trips = [dict(row) for row in data]
    for trip in trips:
        if '알짜 팁' in trip and trip['알짜 팁']:
            trip['알짜 팁'] = '\n'.join('- ' + part.strip() for part in trip['알짜 팁'].split('-') if part)
        
        if '가격' in trip and trip['가격']:
            trip['가격'] = '\n'.join(part.strip() for part in trip['가격'].split('-') if part)
    
    return trips

# forest.db에서 데이터 가져오기
def get_forest_data():
    conn = sqlite3.connect(FOREST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forest")
    columns = [description[0] for description in cursor.description]
    forests = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return forests

# cafe.db에서 데이터 가져오기
def get_cafe_data():
    conn = sqlite3.connect(CAFE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT 지역, 장소, `알짜 팁`, 링크 FROM cafe_locations")
    data = cursor.fetchall()
    conn.close()
    
    cafes = [dict(row) for row in data]
    for cafe in cafes:
        if '알짜 팁' in cafe and cafe['알짜 팁']:
            cafe['알짜 팁'] = '\\n'.join('- ' + part.strip() for part in cafe['알짜 팁'].split('-') if part)
    
    return cafes

@app.route('/')
def index():
    event_data = get_event_data()
    nino_trip_data = get_nino_trip_data()
    forest_data = get_forest_data()
    cafe_data = get_cafe_data()
    
    return render_template('index.html', event_data=event_data, nino_trip_data=nino_trip_data, forest_data=forest_data, cafe_data=cafe_data)

if __name__ == '__main__':
    app.run(debug=True)

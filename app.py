from flask import Flask, render_template
from flask import request, jsonify
import sqlite3
import os

app = Flask(__name__)

# 데이터베이스 파일 경로 설정
EVENT_DB_PATH = os.path.join("data", "event.db")
NINO_TRIP_DB_PATH = os.path.join("data", "nino-trip.db")
FOREST_DB_PATH = os.path.join("data", "forest.db")
CAFE_DB_PATH = os.path.join("data", "cafe.db")
KIDS_RESTAURANT_DB_PATH = os.path.join("data", "kids_restaurant.db")
CULTURE_CENTER_DB_PATH = os.path.join("data", "culture_center.db")
DB_PATH = os.path.join("data", "db.sqlite3")

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
    cursor.execute("SELECT 지역, 장소, [알짜 팁], 링크 FROM cafe_locations")
    data = cursor.fetchall()
    conn.close()

    cafes = [dict(row) for row in data]
    for cafe in cafes:
        if '알짜 팁' in cafe and cafe['알짜 팁']:
            cafe['알짜 팁'] = '\n'.join('- ' + part.strip() for part in cafe['알짜 팁'].split('-') if part)
    
    return cafes

# kids_restaurant.db에서 데이터 가져오기
def get_kids_restaurant_data():
    conn = sqlite3.connect(KIDS_RESTAURANT_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT 장소, [알짜 팁], 링크 FROM kids_restaurant")
    data = cursor.fetchall()
    conn.close()

    kids_restaurants = [dict(row) for row in data]
    for kids_restaurant in kids_restaurants:
        if '알짜 팁' in kids_restaurant and kids_restaurant['알짜 팁']:
            kids_restaurant['알짜 팁'] = '\n'.join('- ' + part.strip() for part in kids_restaurant['알짜 팁'].split('-') if part)
    
    return kids_restaurants

# culture_center.db에서 데이터 가져오기
def get_culture_center_data():
    conn = sqlite3.connect(CULTURE_CENTER_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT 장소, [알짜 팁], 나이, 종류, 가격, 링크 FROM culture_center")
    data = cursor.fetchall()
    conn.close()

    culture_centers = [dict(row) for row in data]
    for culture_center in culture_centers:
        if '알짜 팁' in culture_center and culture_center['알짜 팁']:
            culture_center['알짜 팁'] = '\n'.join('- ' + part.strip() for part in culture_center['알짜 팁'].split('-') if part)
    
    return culture_centers

@app.route('/')
def index():
    event_data = get_event_data()
    nino_trip_data = get_nino_trip_data()
    forest_data = get_forest_data()
    cafe_data = get_cafe_data()
    kids_restaurant_data = get_kids_restaurant_data()
    culture_center_data = get_culture_center_data()

    
    return render_template('index.html', event_data=event_data, nino_trip_data=nino_trip_data, forest_data=forest_data, 
                           cafe_data=cafe_data, kids_restaurant_data=kids_restaurant_data, culture_center_data=culture_center_data)

@app.route('/api/inquiries', methods=['POST'])
def add_inquiry():
    data = request.json
    if not data.get('name') or not data.get('message'):
        return jsonify({'error': '이름과 문의 내용을 모두 입력해 주세요.'}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Inquiry (name, message, response, status) VALUES (?, ?, ?, ?)",
            (data['name'], data['message'], None, '접수 대기 중')
        )
        conn.commit()
        return jsonify({'message': '문의가 성공적으로 접수되었습니다.'}), 201
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/inquiries', methods=['GET'])
def get_inquiries():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, message, response, status FROM Inquiry")
        columns = [description[0] for description in cursor.description]
        inquiries = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(inquiries)
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/inquiries/<int:id>', methods=['PATCH'])
def update_inquiry(id):
    data = request.json
    response = data.get('response')
    if response is None:
        return jsonify({'error': '답변 내용을 입력해 주세요.'}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Inquiry SET response = ?, status = ? WHERE id = ?",
            (response, '답변 완료', id)
        )
        conn.commit()
        return jsonify({'message': '문의가 성공적으로 업데이트되었습니다.'})
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/inquiries/<int:id>', methods=['DELETE'])
def delete_inquiry(id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Inquiry WHERE id = ?", (id,))
        conn.commit()
        return jsonify({'message': '문의가 성공적으로 삭제되었습니다.'}), 200
    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '0819':  # 간단한 4자리 비밀번호
            return render_template('admin.html')  # 관리자 페이지 렌더링
        else:
            return "비밀번호가 틀렸습니다.", 403

    return '''
        <form method="POST">
            <label for="password">비밀번호 입력:</label>
            <input type="password" name="password" required>
            <button type="submit">접속</button>
        </form>
    '''

@app.route('/admin')
def admin_inquiries():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
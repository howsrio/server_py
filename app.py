from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__,
            static_url_path='/static',
            static_folder='Frontend',
            template_folder='Frontend')
CORS(app)

# SQLite 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///preferences.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # 이름 고유값
    preferences = db.Column(db.String(500), nullable=False)

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

# 데이터베이스 초기화 함수
def create_tables():
    with app.app_context():
        db.create_all()

# 메인 페이지 렌더링
@app.route('/')
def index():
    return render_template('HomePage.html')

@app.route('/create_preferences')
def create_preferences():
    return render_template('CreatePreferences.html')

@app.route('/create_meeting')
def create_meeting():
    return render_template('Create_a_meeting.html')

@app.route('/recommend')
def recommend():
    return render_template('Recommend.html')

# 정적 파일 제공 (CSS, JS)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'Frontend'), filename)

# 취향 데이터 저장 또는 덮어쓰기
@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    name = request.form.get('name')
    preferences = request.form.get('preferences')

    if not name or not preferences:
        return jsonify({"status": "error", "message": "Name and preferences are required."}), 400

    existing_user = UserPreference.query.filter_by(name=name).first()
    if existing_user:
        existing_user.preferences = preferences
        message = "Preferences updated successfully."
    else:
        new_user = UserPreference(name=name, preferences=preferences)
        db.session.add(new_user)
        message = "Preferences saved successfully."

    db.session.commit()
    return jsonify({"status": "success", "message": message}), 200

# 친구 데이터 저장
@app.route('/save_friend', methods=['POST'])
def save_friend():
    name = request.form.get('name')

    if not name:
        return jsonify({"status": "error", "message": "Friend name is required."}), 400

    existing_friend = Friend.query.filter_by(name=name).first()
    if existing_friend:
        return jsonify({"status": "error", "message": "Friend already exists."}), 400

    new_friend = Friend(name=name)
    db.session.add(new_friend)
    db.session.commit()
    return jsonify({"status": "success", "message": "Friend saved successfully."}), 200

# 친구 데이터 조회
@app.route('/get_friends', methods=['GET'])
def get_friends():
    friends = Friend.query.all()
    data = [{"id": f.id, "name": f.name} for f in friends]
    return jsonify(data)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

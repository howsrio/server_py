from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')
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

# 데이터베이스 초기화 함수
def create_tables():
    with app.app_context():
        db.create_all()

# 메인 페이지 렌더링
@app.route('/')
def index():
    return render_template('HomePage.html')

# 데이터 저장 또는 덮어쓰기
@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    name = request.form.get('name')
    preferences = request.form.get('preferences')

    if not name or not preferences:
        return jsonify({"status": "error", "message": "Name and preferences are required."}), 400

    # 기존 데이터 확인 및 덮어쓰기
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

# 저장된 데이터 삭제
@app.route('/delete_preferences', methods=['POST'])
def delete_preferences():
    name = request.form.get('name')

    if not name:
        return jsonify({"status": "error", "message": "Name is required."}), 400

    user = UserPreference.query.filter_by(name=name).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success", "message": "Preferences deleted successfully."}), 200
    else:
        return jsonify({"status": "error", "message": "No data found for the given name."}), 404

# 저장된 데이터 조회
@app.route('/view_preferences', methods=['GET'])
def view_preferences():
    preferences = UserPreference.query.all()
    data = [{"id": p.id, "name": p.name, "preferences": p.preferences} for p in preferences]
    return jsonify(data)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

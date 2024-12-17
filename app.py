from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder="frontend", static_folder="frontend")

# 데이터베이스 설정
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///preferences.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# DB 모델
class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    positive_prompt = db.Column(db.Text, nullable=True)
    negative_prompt = db.Column(db.Text, nullable=True)

# 애플리케이션 시작 시 DB 생성
with app.app_context():
    db.create_all()

# 시작 페이지: HomePage.html
@app.route("/")
def home():
    return render_template("HomePage.html")

# CreatePreferences.html 렌더링
@app.route("/create-preferences")
def create_preferences():
    return render_template("CreatePreferences.html")

# 취향 데이터 저장 및 DB 내용 출력
@app.route("/save-preference", methods=["POST"])
def save_preference():
    data = request.json
    name = data.get("name")
    location = data.get("location")
    positive_prompt = data.get("positivePrompt")
    negative_prompt = data.get("negativePrompt")

    # 중복 이름 확인 및 업데이트
    existing_record = Preference.query.filter_by(name=name).first()
    if existing_record:
        existing_record.location = location
        existing_record.positive_prompt = positive_prompt
        existing_record.negative_prompt = negative_prompt
        message = "정보가 변경되었습니다."
    else:
        # 새로운 데이터 저장
        new_pref = Preference(
            name=name,
            location=location,
            positive_prompt=positive_prompt,
            negative_prompt=negative_prompt,
        )
        db.session.add(new_pref)
        message = "데이터가 저장되었습니다."

    db.session.commit()

    # DB 테이블 내용 출력
    print("\n현재 저장된 Preferences 테이블:")
    preferences = Preference.query.all()
    for pref in preferences:
        print(f"ID: {pref.id}, 이름: {pref.name}, 위치: {pref.location}, 선호 기준: {pref.positive_prompt}, 제외 조건: {pref.negative_prompt}")
    print("-" * 50)

    return jsonify({"status": "success", "message": message}), 200


# 정적 파일 경로 설정 (CSS, JS 등)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/get-friends-names", methods=["GET"])
def get_friend_names():
    """친구 이름 목록 반환"""
    try:
        friends = Preference.query.with_entities(Preference.name).all()
        friend_names = [friend.name for friend in friends]
        return jsonify({"names": friend_names})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "친구 이름을 불러오는 중 오류가 발생했습니다."}), 500


@app.route("/get-friend-details", methods=["POST"])
def get_friend_details():
    """선택된 이름에 대한 나머지 속성 반환"""
    try:
        data = request.json
        selected_names = data.get("names", [])

        friends = Preference.query.filter(Preference.name.in_(selected_names)).all()
        friend_details = {
            "name": [friend.name for friend in friends],
            "location": [friend.location for friend in friends],
            "positive_prompt": [friend.positive_prompt for friend in friends],
            "negative_prompt": [friend.negative_prompt for friend in friends],
        }
        return jsonify(friend_details)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "친구 세부 정보를 불러오는 중 오류가 발생했습니다."}), 500


if __name__ == "__main__":
    app.run(debug=True)

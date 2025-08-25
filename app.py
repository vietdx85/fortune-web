from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
import os, random, hashlib, sqlite3
from datetime import datetime
from models import init_db, add_record, get_user_history, search_records

# Load biến môi trường
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret")

init_db()

# Tarot & Zodiac
tarot_cards = [
    "The Fool", "The Magician", "The High Priestess", "The Empress",
    "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
    "Strength", "The Hermit", "Wheel of Fortune", "Justice",
    "The Hanged Man", "Death", "Temperance", "The Devil",
    "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
]

zodiac_predictions = {
    "Aries": "Bạn sẽ gặp may mắn trong công việc.",
    "Taurus": "Một ngày tốt để học hỏi điều mới.",
    "Gemini": "Sự sáng tạo của bạn được phát huy.",
    "Cancer": "Lắng nghe trực giác sẽ giúp bạn.",
    "Leo": "Tự tin sẽ giúp bạn thành công.",
    "Virgo": "Chú ý sức khỏe và nghỉ ngơi.",
    "Libra": "Cân bằng công việc và tình cảm.",
    "Scorpio": "Cơ hội nghề nghiệp xuất hiện.",
    "Sagittarius": "Tận hưởng niềm vui nhỏ.",
    "Capricorn": "Kiên nhẫn mang lại kết quả.",
    "Aquarius": "Thử nghiệm mới giúp tiến bộ.",
    "Pisces": "Dành thời gian cho bản thân và gia đình."
}

# Hàm tính Zodiac
def get_zodiac(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"

# Lucky number
def generate_lucky_number(name):
    today = datetime.now()
    seed = sum(ord(c) for c in name) + today.day + today.month + today.year
    random.seed(seed)
    return random.randint(1, 99)

# Chat history
def add_chat_message(role, message):
    if 'chat_history' not in session:
        session['chat_history'] = []
    session['chat_history'].append({"role": role, "message": message})
    session.modified = True

def generate_chat_reply(user_msg):
    user_msg = user_msg.lower()
    if "tử vi" in user_msg:
        return "Bạn có thể xem tử vi của mình trên trang xem bói."
    elif "tarot" in user_msg:
        return "Bạn có thể rút bài tarot 3 lá để biết quá khứ, hiện tại, tương lai."
    elif "may mắn" in user_msg:
        return f"Số may mắn hôm nay của bạn là {random.randint(1, 99)}."
    else:
        return "Mình có thể trả lời các câu hỏi về bói, tử vi, tarot, hoặc số may mắn."

# Routes
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, hashed_pw))
            conn.commit(); conn.close()
            return redirect(url_for('login'))
        except:
            return "Username đã tồn tại"
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect('database.db'); c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed_pw))
        row = c.fetchone(); conn.close()
        if row:
            session['user_id']=row[0]; session['username']=username
            return redirect(url_for('index'))
        else:
            return "Sai thông tin đăng nhập"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/", methods=["GET","POST"])
def index():
    if 'user_id' not in session: return redirect(url_for('login'))
    result = None
    if request.method=="POST":
        name = request.form.get("name")
        birthdate = request.form.get("birthdate")
        bok_type = request.form.get("type")
        if name and birthdate:
            dt = datetime.strptime(birthdate, "%Y-%m-%d")
            zodiac = get_zodiac(dt.month, dt.day)
            tarot_draw = random.sample(tarot_cards,3)
            lucky_number = generate_lucky_number(name)
            result = {
                "name": name, "birthdate": birthdate, "zodiac": zodiac,
                "prediction": zodiac_predictions[zodiac],
                "tarot": tarot_draw, "lucky_number": lucky_number,
                "type": bok_type
            }
            add_record(result, session['user_id'])
    return render_template("index.html", result=result)

@app.route("/history")
def history():
    if 'user_id' not in session: return redirect(url_for('login'))
    records = get_user_history(session['user_id'])
    return render_template("history.html", records=records)

@app.route("/search", methods=["GET"])
def search():
    if 'user_id' not in session: return redirect(url_for('login'))
    q = request.args.get("q","")
    records = search_records(q)
    return render_template("history.html", records=records, query=q)

@app.route("/chat")
def chat():
    if 'user_id' not in session: return redirect(url_for('login'))
    chat_history = session.get('chat_history',[])
    return render_template("chat.html", chat_history=chat_history)

@app.route("/chat/send", methods=["POST"])
def chat_send():
    if 'user_id' not in session: return jsonify({"error":"Not logged in"}),401
    user_msg = request.json.get("message")
    add_chat_message("user", user_msg)
    response_msg = generate_chat_reply(user_msg)
    add_chat_message("bot", response_msg)
    return jsonify({"reply": response_msg})

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    records = get_user_history(session['user_id'])
    history_count = len(records)
    chat_count = len(session.get('chat_history',[]))
    lucky_today = generate_lucky_number(session['username'])
    return render_template("dashboard.html",
                           records=records,
                           history_count=history_count,
                           chat_count=chat_count,
                           lucky_today=lucky_today)

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
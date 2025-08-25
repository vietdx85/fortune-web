from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Dữ liệu bói ví dụ
predictions = [
    "Hôm nay là một ngày may mắn của bạn!",
    "Cẩn thận trong công việc hôm nay.",
    "Một cơ hội bất ngờ sẽ đến với bạn.",
    "Hãy tin vào trực giác của bản thân.",
    "Sẽ có tin vui về tài chính."
]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            result = f"{name}, {random.choice(predictions)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    # Lắng nghe trên tất cả IP (để truy cập từ bên ngoài WSL)
    app.run(host="0.0.0.0", port=5000, debug=True)
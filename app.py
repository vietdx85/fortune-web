from flask import Flask, render_template, request
import random
from datetime import datetime

app = Flask(__name__)

# Dữ liệu bói mẫu
tarot_cards = [
    "The Fool - Bắt đầu mới",
    "The Magician - Sáng tạo, quyền lực",
    "The Lovers - Tình yêu, lựa chọn",
    "The Sun - Hạnh phúc, thành công",
    "Death - Kết thúc, thay đổi"
]

lucky_numbers = [str(i) for i in range(1, 50)]

zodiac_predictions = {
    "Aries": "Hôm nay bạn nên cẩn thận trong các quyết định tài chính.",
    "Taurus": "Một ngày tốt để gặp gỡ bạn bè và học hỏi điều mới.",
    "Gemini": "Tinh thần sáng tạo của bạn sẽ được phát huy.",
    "Cancer": "Hãy lắng nghe trực giác của bạn hôm nay.",
    "Leo": "Sự tự tin sẽ giúp bạn giải quyết khó khăn.",
    "Virgo": "Chú ý đến sức khỏe và nghỉ ngơi hợp lý.",
    "Libra": "Cân bằng giữa công việc và tình cảm.",
    "Scorpio": "Một cơ hội nghề nghiệp mới sẽ xuất hiện.",
    "Sagittarius": "Hãy tận hưởng những niềm vui nhỏ.",
    "Capricorn": "Kiên nhẫn sẽ mang lại kết quả tốt.",
    "Aquarius": "Thử nghiệm điều mới sẽ giúp bạn tiến bộ.",
    "Pisces": "Hãy dành thời gian cho bản thân và gia đình."
}

# Hàm xác định cung hoàng đạo từ ngày sinh
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

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        name = request.form.get("name")
        birthdate = request.form.get("birthdate")  # YYYY-MM-DD
        if name and birthdate:
            dt = datetime.strptime(birthdate, "%Y-%m-%d")
            zodiac = get_zodiac(dt.month, dt.day)
            result['name'] = name
            result['zodiac'] = zodiac
            result['prediction'] = zodiac_predictions[zodiac]
            result['tarot'] = random.choice(tarot_cards)
            result['lucky_number'] = random.choice(lucky_numbers)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    # Lắng nghe trên tất cả IP (để truy cập từ bên ngoài WSL)
    app.run(host="0.0.0.0", port=5000, debug=True)
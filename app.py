from flask import Flask, render_template, request
import pandas as pd
import random
import os

app = Flask(__name__)

# ✅ تحميل بيانات التعريفات من ملف Excel
def load_legal_definitions():
    file_path = "legal_definitions.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return dict(zip(df['المصطلح'], df['التعريف']))
    return {}

legal_definitions = load_legal_definitions()

# ✅ عبارات ترحيب وإغلاق
opening_phrases = ["🔹 رفيقي العزيز، الجواب على سؤالك هو:", "🔹 صديقي القانوني، إليك الإجابة:"]
closing_phrases = ["💡 هل لديك استفسار آخر؟ أنا هنا للمساعدة!", "⚖️ إن كنت بحاجة إلى توضيح أكثر، لا تتردد في السؤال!"]

# ✅ دالة البحث عن تعريف
def find_legal_definition(query):
    for key, definition in legal_definitions.items():
        if key in query:
            return f"{random.choice(opening_phrases)}\n\n📘 **{key}:** {definition}\n\n{random.choice(closing_phrases)}"
    return "❌ حسناً، لا أملك إجابة على سؤالك حالياً، يمكنك تجربة مصطلح آخر."

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        query = request.form["query"]
        response = find_legal_definition(query)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # تعيين المنفذ
    app.run(host="0.0.0.0", port=port, debug=True)


from flask import Flask, render_template, request
import pandas as pd
import random
import os
from sentence_transformers import SentenceTransformer, util  # 🔥 مكتبة الذكاء الاصطناعي

app = Flask(__name__)

# ✅ تحميل بيانات التعريفات من ملف Excel
def load_legal_definitions():
    file_path = "legal_definitions.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return dict(zip(df['المصطلح'], df['التعريف']))
    return {}

legal_definitions = load_legal_definitions()

# ✅ تحميل نموذج الذكاء الاصطناعي (BERT محسن)
model = SentenceTransformer('all-MiniLM-L6-v2')

# ✅ تجهيز التمثيلات العددية (Embeddings) للتعاريف
terms = list(legal_definitions.keys())  # المصطلحات القانونية
definitions = list(legal_definitions.values())  # التعريفات
term_embeddings = model.encode(terms, convert_to_tensor=True)

# ✅ عبارات ترحيب وإغلاق
opening_phrases = ["🔹 رفيقي العزيز، الجواب على سؤالك هو:", "🔹 صديقي القانوني، إليك الإجابة:"]
closing_phrases = ["💡 هل لديك استفسار آخر؟ أنا هنا للمساعدة!", "⚖️ إن كنت بحاجة إلى توضيح أكثر، لا تتردد في السؤال!"]

# ✅ دالة البحث باستخدام الذكاء الاصطناعي
def find_legal_definition(query):
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, term_embeddings)[0]  # حساب التشابه
    best_match_idx = similarities.argmax().item()  # العثور على أقرب مصطلح قانوني
    best_match_term = terms[best_match_idx]  # المصطلح الأكثر تطابقًا
    best_match_definition = definitions[best_match_idx]  # التعريف المقابل
    
    # التأكد من أن التشابه عالٍ بما يكفي ليكون الجواب منطقيًا
    if similarities[best_match_idx] < 0.5:  
        return "❌ لم أتمكن من العثور على إجابة دقيقة لسؤالك. حاول بصياغة أخرى."

    return f"{random.choice(opening_phrases)}\n\n📘 **{best_match_term}:** {best_match_definition}\n\n{random.choice(closing_phrases)}"

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


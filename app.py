from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import re
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def split_text(text, max_length=1000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.json or {}
        text = data.get("text", "").strip()
        source_lang = data.get("source", "auto")
        target_lang = data.get("target", "ar")

        if not text:
            return jsonify({"result": "⚠️ Empty text"})

        chunks = split_text(text)
        translated_parts = []

        for chunk in chunks:
            try:
                translated = GoogleTranslator(
                    source=source_lang,
                    target=target_lang
                ).translate(chunk)
                translated_parts.append(translated)
            except Exception as inner_error:
                print("Chunk error:", inner_error)
                translated_parts.append(chunk)

        translated_text = " ".join(translated_parts)

        return jsonify({
            "result": translated_text,
            "from": source_lang,
            "to": target_lang
        })

    except Exception as e:
        print("Fatal error:", e)
        return jsonify({"result": "Server error"})

# للاستضافة - استخدم PORT من البيئة
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, render_template, request, jsonify
import json
import os
import difflib
from datetime import datetime

app = Flask(__name__)

with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"].lower().strip()

    meilleure_reponse = None
    meilleur_score = 0

    for item in faq:
        question_type = item["question"].lower()
        mots_cles = item["mots_cles"]
        reponse = item["reponse"]

        score = difflib.SequenceMatcher(None, message, question_type).ratio()

        for mot in mots_cles:
            if mot.lower() in message:
                score += 0.35

        if score > meilleur_score:
            meilleur_score = score
            meilleure_reponse = reponse

    if meilleur_score >= 0.35:
        return jsonify({"reply": meilleure_reponse})

    enregistrer_question_inconnue(message)

    return jsonify({
        "reply": "Je n'ai pas encore cette information. Vous pouvez contacter le loueur directement."
    })

def enregistrer_question_inconnue(question):
    fichier = "questions_inconnues.json"

    data = []

    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)

    data.append({
        "question": question,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
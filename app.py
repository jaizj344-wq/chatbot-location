from flask import Flask, render_template, request, jsonify
import json
import os
import re
import unicodedata
from datetime import datetime

app = Flask(__name__)

with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

def normaliser(texte):
    texte = texte.lower()
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return texte

def contient_mot_entier(message, mot_cle):
    message = normaliser(message)
    mot_cle = normaliser(mot_cle)

    pattern = r"(^|[^a-zA-Z0-9])" + re.escape(mot_cle) + r"([^a-zA-Z0-9]|$)"
    return re.search(pattern, message) is not None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]

    for item in faq:
        for mot in item["mots_cles"]:
            if contient_mot_entier(message, mot):
                return jsonify({"reply": item["reponse"]})

    enregistrer_question_inconnue(message)

    return jsonify({
        "reply": "Je n'ai pas compris votre question. Pouvez-vous reformuler ou contacter le loueur directement ?"
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
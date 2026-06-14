from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Charger les données du client
with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"].lower()

    # Recherche simple dans les clés
    for key in faq:
        if key in message:
            return jsonify({"reply": faq[key]})

    return jsonify({"reply": "Je n'ai pas encore la réponse à cette question. Pouvez-vous reformuler ?"})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
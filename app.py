from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Chargement de la FAQ
with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    message = request.json["message"].lower()

    mots_cles = {
        "prix": ["prix", "tarif", "coût", "cout"],
        "caution": ["caution", "garantie", "depot", "dépôt"],
        "franchise": ["franchise"],
        "assurance": ["assurance", "assuré", "couverture"],
        "age": ["âge", "age", "jeune conducteur"],
        "permis": ["permis", "ancienneté"],
        "documents": ["document", "documents", "papier", "pièce d'identité", "identité"],
        "kilometrage": ["kilometrage", "kilométrage", "kilometre", "kilomètre", "km"],
        "carburant": ["carburant", "essence", "plein"],
        "annulation": ["annulation", "annuler"],
        "devis": ["devis"],
        "vehicule": ["vehicule", "véhicule", "modèle", "modele"],
        "retour": ["retour", "restitution"],
        "dommage": ["dommage", "accident", "rayure"],
        "conducteur": ["conducteur", "conductrice"],
        "livraison": ["livraison"]
    }

    for categorie, mots in mots_cles.items():
        for mot in mots:
            if mot in message:
                return jsonify({
                    "reply": faq.get(
                        categorie,
                        "Je n'ai pas encore cette information."
                    )
                })

    return jsonify({
        "reply": "Je n'ai pas trouvé la réponse à votre question. Merci de reformuler votre demande."
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
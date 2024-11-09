from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis d'autres origines (pour un accès via le navigateur du téléphone)

DATA_FILE = "fiches.json"

def lire_fiches():
    """Charge les fiches de révision depuis un fichier JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def ecrire_fiches(fiches):
    """Sauvegarde les fiches de révision dans un fichier JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(fiches, f, indent=4)

@app.route('/fiches', methods=['GET'])
def get_fiches():
    """Récupère toutes les fiches de révision."""
    fiches = lire_fiches()
    return jsonify(fiches)

@app.route('/fiches', methods=['POST'])
def add_fiche():
    """Ajoute une nouvelle fiche de révision."""
    data = request.get_json()
    titre = data.get("titre")
    contenu = data.get("contenu")

    if not titre or not contenu:
        return jsonify({"error": "Titre et contenu sont requis."}), 400

    fiches = lire_fiches()
    fiche = {"id": len(fiches) + 1, "titre": titre, "contenu": contenu}
    fiches.append(fiche)
    ecrire_fiches(fiches)
    return jsonify(fiche), 201

@app.route('/fiches/<int:fiche_id>', methods=['DELETE'])
def delete_fiche(fiche_id):
    """Supprime une fiche de révision par son ID."""
    fiches = lire_fiches()
    fiches = [f for f in fiches if f["id"] != fiche_id]
    ecrire_fiches(fiches)
    return jsonify({"message": "Fiche supprimée"}), 200

if __name__ == '__main__':
    app.run(debug=True)

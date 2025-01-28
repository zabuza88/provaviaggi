from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@app.route("/api/optimize", methods=["POST"])
def optimize_route():
    data = request.json
    places = data.get("places", [])
    transport_modes = data.get("transportModes", ["driving"])

    if len(places) < 2:
        return jsonify({"error": "Aggiungi almeno due posti"}), 400

    try:
        # Chiamata a Google Distance Matrix API
        response = requests.get(
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            params={
                "origins": "|".join(places),
                "destinations": "|".join(places),
                "key": GOOGLE_MAPS_API_KEY,
                "mode": transport_modes[0],
            },
        )
        response_data = response.json()

        if "rows" not in response_data:
            return jsonify({"error": "Errore nel calcolo del percorso"}), 500

        # Processa i dati per restituire un risultato semplice
        routes = []
        for i, place in enumerate(places):
            routes.append({
                "place": place,
                "time": response_data["rows"][i]["elements"][i]["duration"]["text"],
                "mode": transport_modes[0],
            })

        return jsonify({"routes": routes})

    except Exception as e:
        print(e)
        return jsonify({"error": "Errore interno"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

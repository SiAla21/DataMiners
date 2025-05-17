from flask import Flask, jsonify
from flask_cors import CORS
from position_model import PositionRecommender  # Custom model with internal club lookup

app = Flask(__name__)
CORS(app)

# Load model and dataset
model = PositionRecommender("clubs_n.csv")

# ---- GET /predict/<club_name> ----
@app.route('/predict/<club_name>', methods=['GET'])
def predict(club_name):
    try:
        if not club_name:
            return jsonify({"error": "Missing club name"}), 400

        prediction = model.predict(club_name)

            # Ensure it's a dictionary with top_5_weakest_positions directly at top level
        if isinstance(prediction, dict):
            return jsonify(prediction)
        else:
            return jsonify({
        "club": club_name,
        "top_5_weakest_positions": prediction
    })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---- GET /club-details/<club_name> ----
@app.route('/club-details/<club_name>', methods=['GET'])
def club_details(club_name):
    try:
        if not club_name:
            return jsonify({"error": "Missing club name"}), 400

        # Case-insensitive match
        match = model.df[model.df["club"].str.lower() == club_name.lower()]
        if match.empty:
            return jsonify({"error": f"Club '{club_name}' not found."}), 404

        return jsonify(match.iloc[0].to_dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---- Run Server ----
if __name__ == '__main__':
    app.run(debug=True, port=5000)

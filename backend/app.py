from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from condition_extractor import ConditionExtractor
from football_recommender import FootballRecommender

app = Flask(__name__)
CORS(app)

# ✅ Initialisation
players = pd.read_csv("Players_Used_Columns.csv")
coaches = pd.read_csv("Coaches_Used_Columns.csv")
doctors = pd.read_csv("Doctors_Used_Columns.csv")

extractor = ConditionExtractor(players, coaches, doctors)
recommender = FootballRecommender(
    players_file="Players_Used_Columns.csv",
    transfers_file="Transfers_Used_Columns.csv",
    clubs_file="clubs_n.csv",
    coaches_file="Coaches_Used_Columns.csv",
    doctors_file="Doctors_Used_Columns.csv"
)

# ✅ Routes
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue sur l'API de recommandation."})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    text = data.get("text")
    club = data.get("club", "ajax")
    result = extractor.extract_all(text)
    profile = result['profile']
    conditions = result['conditions']
    print(f"✅ Profil : {profile}")
    print(f"✅ Conditions extraites : {conditions}")

    if profile == 'player':
        position = None
        for col, op, val in conditions:
            if col == 'registered_position' and op == '==':
                position = val
        print(f"✅ Position détectée : {position}")

        df = recommender.recommend_players_for_club(club, position=position, top_n=5)

        if df.empty:
            return jsonify({
                "results": [],
                "profile": profile,
                "conditions": conditions,
                "message": f"❌ Aucun joueur trouvé pour le club '{club}' ou la position '{position}'."
            })

        df = recommender.filter_players_by_conditions(df, conditions)

        if df.empty:
            return jsonify({
                "results": [],
                "profile": profile,
                "conditions": conditions,
                "message": f"❌ Aucun joueur ne correspond à toutes les conditions."
            })

        base_cols = ['name', 'team_name', 'league', 'registered_position', 'similarity_score']
        condition_cols = list({col for col, _, _ in conditions})
        cols_to_show = base_cols + [col for col in condition_cols if col in df.columns]
        cols_to_show = list(dict.fromkeys(cols_to_show))

        df = df[cols_to_show]

        return jsonify({
            "results": df.to_dict(orient="records"),
            "profile": profile,
            "conditions": conditions
        })


    elif profile == 'coach':
        formation = None

        for col, op, val in conditions:
            if col == 'preffered_formation':
                formation = val.lower().strip()

        if not formation:
            return jsonify({
                "results": [],
                "profile": profile,
                "conditions": conditions,
                "message": "❌ Aucune formation détectée par LLM."
            })

        # 🎯 Étape 1 : générer la table avec uniquement la formation
        df = recommender.recommend_coaches_by_formation(formation, top_n=100)

        if df.empty:
            return jsonify({
                "results": [],
                "profile": profile,
                "conditions": conditions,
                "message": f"❌ Aucun coach trouvé avec la formation '{formation}'."
            })

        # 🎯 Étape 2 : appliquer les conditions sur cette table (âge, licence...)
        filtered_df = recommender.filter_dataframe(df.copy(), conditions)

        if filtered_df.empty:
            return jsonify({
                "results": [],
                "profile": profile,
                "conditions": conditions,
                "message": "❌ Aucun coach ne correspond aux filtres supplémentaires."
            })

        # Ajouter style si manquant
        if 'style' not in filtered_df.columns and 'preffered_formation' in filtered_df.columns:
            filtered_df['style'] = filtered_df['preffered_formation'].map(recommender.formation_to_style)

        # Ajouter similarité si manquante
        if 'similarity_score' not in filtered_df.columns:
            filtered_df['similarity_score'] = 0.5

        return jsonify({
            "results": filtered_df.head(5).to_dict(orient="records"),
            "profile": profile,
            "conditions": conditions
        })

        return jsonify([])

    elif profile == 'doctor':
        df = recommender.recommend_doctors_for_club(club, top_n=5)
        return jsonify(df.to_dict(orient="records"))

    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)

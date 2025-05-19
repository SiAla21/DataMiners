from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from condition_extractor import ConditionExtractor
from football_recommender import FootballRecommender

app = Flask(__name__)
CORS(app)

# Chargement des données CSV (chemins à adapter)
players = pd.read_csv("Players_Used_Columns.csv")
coaches = pd.read_csv("Coaches_Used_Columns.csv")
doctors = pd.read_csv("Doctors_Used_Columns.csv")

# Ajouter colonne 'club' identique à 'team_name' si pas déjà
if 'club' not in players.columns and 'team_name' in players.columns:
    players['club'] = players['team_name']

extractor = ConditionExtractor(players, coaches, doctors)
recommender = FootballRecommender(
    players_file="Players_Used_Columns.csv",
    transfers_file="Transfers_Used_Columns.csv",
    clubs_file="clubs_n.csv",
    coaches_file="Coaches_Used_Columns.csv",
    doctors_file="Doctors_Used_Columns.csv"
)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    text = data.get("text", "")
    club = data.get("club", "ajax").lower().strip()

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
                "message": "❌ Aucun joueur ne correspond à toutes les conditions."
            })

        base_cols = ['name', 'club', 'league', 'registered_position', 'similarity_score']
        existing_cols = [col for col in base_cols if col in df.columns]
        condition_cols = list({col for col, _, _ in conditions if col in df.columns})
        cols_to_show = existing_cols + [col for col in condition_cols if col not in existing_cols]
        df = df[cols_to_show]

        df = df.fillna('N/A')

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
                "message": "❌ Aucune formation détectée."
            })

        df = recommender.recommend_coaches_by_formation(formation, top_n=100)
        if df.empty:
            return jsonify({
                "results": [],
                "profile": profile,
                "conditions": conditions,
                "message": f"❌ Aucun coach trouvé avec la formation '{formation}'."
            })

        filtered_df = recommender.filter_dataframe(df.copy(), conditions)
        if filtered_df.empty:
            return jsonify({
                "results": [],
                "profile": profile,
                "conditions": conditions,
                "message": "❌ Aucun coach ne correspond aux filtres supplémentaires."
            })

        if 'style' not in filtered_df.columns and 'preffered_formation' in filtered_df.columns:
            filtered_df['style'] = filtered_df['preffered_formation'].map(recommender.formation_to_style)
        if 'similarity_score' not in filtered_df.columns:
            filtered_df['similarity_score'] = 0.5

        cols_to_return = ['name', 'club', 'age', 'avg_term_as_coach', 'preffered_formation', 'coaching_licence', 'style', 'similarity_score']
        print("DEBUG colonnes avant filtrage:", filtered_df.columns.tolist())
        print("DEBUG colonnes demandées:", cols_to_return)

        cols_to_return = [col for col in cols_to_return if col in filtered_df.columns]
        filtered_df = filtered_df[cols_to_return]

        filtered_df = filtered_df.fillna('N/A')

        return jsonify({
            "results": filtered_df.head(5).to_dict(orient="records"),
            "profile": profile,
            "conditions": conditions
        })

    elif profile == 'doctor':
        df = recommender.recommend_doctors_for_club(club, top_n=5)
        cols_to_return = ['Rndrng_Prvdr_First_Name', 'Rndrng_Prvdr_Last_Org_Name', 'Rndrng_Prvdr_Type', 'similarity_score']
        cols_to_return = [col for col in cols_to_return if col in df.columns]
        df = df[cols_to_return]
        df = df.fillna('N/A')

        return jsonify({
            "results": df.to_dict(orient="records"),
            "profile": profile,
            "conditions": conditions
        })

    return jsonify({
        "results": [],
        "message": "Profil inconnu ou non supporté."
    })

if __name__ == '__main__':
    app.run(debug=True)

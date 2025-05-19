# === football_recommender.py ===
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

class FootballRecommender:
    def __init__(self, players_file, transfers_file, clubs_file, coaches_file, doctors_file):
        self.formation_to_style = {
            '4-3-3 attacking': 'offensif', '3-4-2-1': 'offensif', '4-2-3-1': 'Balanced',
            '4-1-4-1': 'equilibre', '4-4-2 double 6': 'equilibre', '4-3-1-2': 'equilibre',
            '3-5-2 flat': 'equilibre', '4-4-2': 'equilibre', '5-3-2': 'defensif',
            '4-4-2 diamond': 'equilibre', '3-4-1-2': 'offensif'
        }

        self.players_df = pd.read_csv(players_file, sep=None, engine='python')
        self.transfers_df = pd.read_csv(transfers_file, sep=None, engine='python')
        self.clubs_df = pd.read_csv(clubs_file, sep=None, engine='python')
        self.coaches_df = pd.read_csv(coaches_file, sep=None, engine='python')
        self.doctors_df = pd.read_csv(doctors_file, sep=None, engine='python')

        self.clean_data()
        print("✅ Fichiers chargés.")
        self.build_club_profiles()


    def filter_dataframe(self, df, conditions):
        for col, op, val in conditions:
            if col not in df.columns:
                continue
            from fuzzywuzzy import fuzz

            if op == '==':
                if col == 'coaching_licence':
                    df = df[df[col].apply(lambda x: fuzz.token_set_ratio(str(x), str(val)) >= 90)]
                else:
                    df = df[df[col] == val]

            elif op == '>':
                df = df[df[col] > val]
            elif op == '<':
                df = df[df[col] < val]
            elif op == '>=':
                df = df[df[col] >= val]
            elif op == '<=':
                df = df[df[col] <= val]
        return df
    def filter_players_by_conditions(self, df, conditions):
        for col, op, val in conditions:
            if col == 'registered_position':
                continue

            if col not in self.players_df_raw.columns:
                continue

            try:
                # Utiliser les vraies valeurs non normalisées
                original_vals = self.players_df_raw.loc[df.index, col]
                if op == '==':
                    df = df[original_vals == val]
                elif op == '>':
                    df = df[original_vals > val]
                elif op == '<':
                    df = df[original_vals < val]
                elif op == '>=':
                    df = df[original_vals >= val]
                elif op == '<=':
                    df = df[original_vals <= val]
            except Exception as e:
                print(f"⚠️ Erreur de filtrage pour {col} {op} {val}: {e}")
        return df


    def clean_data(self):
        self.players_df.dropna(subset=['team_name', 'league'], inplace=True)
        self.players_df['team_name'] = self.players_df['team_name'].str.lower().str.strip()
        self.players_df['name'] = self.players_df['name'].str.lower().str.strip()

        # ✅ Nettoyage préalable des valeurs
        self.transfers_df['player_name'] = self.transfers_df['player_name'].astype(str).str.strip()
        self.transfers_df['standardized_club'] = self.transfers_df['standardized_club'].astype(str).str.strip()

        # ✅ Affichage de debug (facultatif)
        print("➡️ Colonnes de transfers_df:", self.transfers_df.columns.tolist())
        print("➡️ Lignes vides dans transfers_df:")
        print(self.transfers_df[self.transfers_df[['player_name', 'standardized_club']].isna().any(axis=1)])

        self.transfers_df.dropna(subset=['player_name', 'standardized_club'], inplace=True)
        self.transfers_df['standardized_club'] = self.transfers_df['standardized_club'].str.lower().str.strip()
        self.transfers_df['player_name'] = self.transfers_df['player_name'].str.lower().str.strip()

        self.clubs_df['club'] = self.clubs_df['club'].str.lower().str.strip()

        self.coaches_df_clean = self.coaches_df.dropna(subset=['preffered_formation', 'coaching_licence', 'club']).copy()
        self.coaches_df_clean['club'] = self.coaches_df_clean['club'].str.lower().str.strip()

        reference_clubs = self.clubs_df['club'].dropna().unique()
        def fuzzy_match_club(club_name, reference_clubs, threshold=80):
            match, score = process.extractOne(club_name, reference_clubs)
            return match if score >= threshold else None

        club_mapping = {club: fuzzy_match_club(club, reference_clubs) for club in self.coaches_df_clean['club'].unique()}
        self.coaches_df_clean['standardized_club'] = self.coaches_df_clean['club'].map(club_mapping)
        self.coaches_df_clean.dropna(subset=['standardized_club'], inplace=True)

        formation_encoder = LabelEncoder()
        licence_encoder = LabelEncoder()

        self.coaches_df_clean['formation_encoded'] = formation_encoder.fit_transform(self.coaches_df_clean['preffered_formation'])
        self.coaches_df_clean['licence_encoded'] = licence_encoder.fit_transform(self.coaches_df_clean['coaching_licence'])

        scaler = MinMaxScaler()
        self.coaches_df_clean['avg_term_as_coach'] = scaler.fit_transform(self.coaches_df_clean[['avg_term_as_coach']])

        self.coaches_df_clean['preffered_formation'] = self.coaches_df_clean['preffered_formation'].str.lower().str.strip()
        self.coaches_df_clean['style'] = self.coaches_df_clean['preffered_formation'].map(self.formation_to_style)
        self.coaches_df_clean['coaching_licence'] = self.coaches_df_clean['coaching_licence'].str.lower().str.strip()

        self.player_features = [
            'age', 'speed', 'acceleration', 'dribbling', 'ball_control',
            'low_pass', 'finishing', 'defensive_awareness', 'physical_contact',
            'stamina', 'kicking_power', 'heading', 'tight_possession'
        ]
        self.player_features = [f for f in self.player_features if f in self.players_df.columns]

        self.players_df[self.player_features] = self.players_df[self.player_features].fillna(0)
        # Garde une copie brute pour les conditions
        self.players_df_raw = self.players_df.copy()

        # Normalise juste pour la similarité (pas pour le filtrage)
        self.players_df[self.player_features] = scaler.fit_transform(self.players_df[self.player_features])


        print("\u2705 Données nettoyées.")


    def build_club_profiles(self):
        self.club_profiles = {}
        for club in self.transfers_df['standardized_club'].unique():
            club_players = self.transfers_df[self.transfers_df['standardized_club'] == club]['player_name'].unique()
            matched_players = self.players_df[self.players_df['name'].isin(club_players)]
            if not matched_players.empty:
                profile_vector = matched_players[self.player_features].mean(axis=0).values
                self.club_profiles[club] = profile_vector
        print(f"\u2705 {len(self.club_profiles)} profils de clubs créés.")
    def recommend_coaches_by_formation_and_licence(self, formation, licence, top_n=5):
        formation = formation.lower().strip()
        licence = licence.lower().strip()

        temp_df = self.coaches_df_clean.copy()
        temp_df = temp_df[
            (temp_df['preffered_formation'] == formation) &
            (temp_df['coaching_licence'].str.lower().str.strip() == licence)
        ]

        if temp_df.empty:
            print(f"❌ Aucun coach trouvé avec formation '{formation}' et licence '{licence}'.")
            return pd.DataFrame()

        ideal_vector = np.array([[0.5, 0.5, temp_df['formation_encoded'].median(), temp_df['licence_encoded'].median()]])
        similarities = cosine_similarity(temp_df[['age', 'avg_term_as_coach', 'formation_encoded', 'licence_encoded']], ideal_vector).flatten()
        temp_df['similarity_score'] = similarities

        return temp_df.sort_values(by='similarity_score', ascending=False).head(top_n)

    def recommend_players_for_club(self, club_name, position=None, top_n=5):
        club_name = club_name.lower().strip()
        if club_name not in self.club_profiles:
            print(f"\u274c Aucun profil trouvé pour '{club_name}'.")
            return pd.DataFrame()

        club_vector = self.club_profiles[club_name].reshape(1, -1)
        temp_df = self.players_df.copy()

        if position:
            temp_df = temp_df[temp_df['registered_position'] == position.upper()]
            if temp_df.empty:
                print(f"\u274c Aucun joueur trouvé pour la position '{position}'.")
                return pd.DataFrame()

        similarities = cosine_similarity(temp_df[self.player_features], club_vector).flatten()
        temp_df['similarity_score'] = similarities

        # ✅ Garder toutes les colonnes (ne pas filtrer ici)
        return temp_df.sort_values(by='similarity_score', ascending=False).head(top_n)

    def recommend_coaches_by_formation(self, formation, top_n=5):
        formation = formation.lower().strip()
        temp_df = self.coaches_df_clean.copy()

        if formation not in temp_df['preffered_formation'].values:
            print(f"❌ Aucun coach trouvé avec la formation '{formation}'.")
            return pd.DataFrame()

        temp_df = temp_df[temp_df['preffered_formation'] == formation]

        # Génère un vecteur idéal (médian des valeurs numériques pour cette formation)
        ideal_vector = np.array([[0.5, 0.5, temp_df['formation_encoded'].median(), temp_df['licence_encoded'].median()]])
        similarities = cosine_similarity(temp_df[['age', 'avg_term_as_coach', 'formation_encoded', 'licence_encoded']], ideal_vector).flatten()
        temp_df['similarity_score'] = similarities

        return temp_df.sort_values(by='similarity_score', ascending=False).head(top_n)

    def recommend_coaches_by_style(self, style=None, licence=None, top_n=5):
        temp_df = self.coaches_df_clean.copy()

        if style:
            temp_df = temp_df[temp_df['style'] == style.lower()]

        if licence:
            temp_df = temp_df[temp_df['coaching_licence'].str.lower().str.strip() == licence.lower().strip()]


        if temp_df.empty:
            print(f"❌ Aucun coach trouvé avec style '{style}' et licence '{licence}'.")
            return pd.DataFrame()

        ideal_vector = np.array([[0.5, 0.5, temp_df['formation_encoded'].median(), temp_df['licence_encoded'].median()]])
        similarities = cosine_similarity(temp_df[['age', 'avg_term_as_coach', 'formation_encoded', 'licence_encoded']], ideal_vector).flatten()
        temp_df['similarity_score'] = similarities

        return temp_df.sort_values(by='similarity_score', ascending=False).head(top_n)[[
            'club', 'age', 'avg_term_as_coach', 'style', 'similarity_score'
        ]]

    def recommend_coaches_for_club_by_style(self, club_name, top_n=5):
        club_name = club_name.lower().strip()
        temp_df = self.coaches_df_clean.copy()
        club_row = temp_df[temp_df['standardized_club'] == club_name]

        if club_row.empty:
            print(f"\u274c Aucun coach actuel trouvé pour '{club_name}'.")
            return pd.DataFrame()

        coach_formation = club_row.iloc[0]['preffered_formation']
        coach_style = self.formation_to_style.get(coach_formation, None)

        if coach_style is None:
            print(f"\u274c Formation '{coach_formation}' inconnue.")
            return pd.DataFrame()

        temp_df = temp_df[temp_df['style'] == coach_style]

        ideal_vector = np.array([[0.5, 0.5, temp_df['formation_encoded'].median(), temp_df['licence_encoded'].median()]])
        similarities = cosine_similarity(temp_df[['age', 'avg_term_as_coach', 'formation_encoded', 'licence_encoded']], ideal_vector).flatten()
        temp_df['similarity_score'] = similarities

        return temp_df.sort_values(by='similarity_score', ascending=False).head(top_n)[[
            'name', 'club', 'age', 'avg_term_as_coach', 'preffered_formation', 'coaching_licence', 'style', 'similarity_score'
        ]]
    def recommend_coaches_by_style_and_optional_licence(self, style, licence=None, top_n=5):
        df = self.coaches_df_clean.copy()
        df = df[df['style'] == style]

        if licence:
            df = df[df['coaching_licence'].str.lower() == licence.lower()]

        if df.empty:
            return pd.DataFrame()

        ideal_vector = np.array([[0.5, 0.5, df['formation_encoded'].median(), df['licence_encoded'].median()]])
        similarities = cosine_similarity(df[['age', 'avg_term_as_coach', 'formation_encoded', 'licence_encoded']], ideal_vector).flatten()
        df['similarity_score'] = similarities

        return df.sort_values(by='similarity_score', ascending=False).head(top_n)

    def recommend_doctors_for_club(self, club_name, top_n=5):
        club_name = club_name.lower().strip()
        club_row = self.clubs_df[self.clubs_df['club'] == club_name]

        if club_row.empty:
            print(f"❌ Aucun club trouvé '{club_name}'.")
            return pd.DataFrame()

        club_total_injuries = club_row.iloc[0]['total_injuries']
        club_average_age = club_row.iloc[0]['average_age']

        temp_doctors = self.doctors_df.dropna(subset=['Tot_Benes', 'Bene_Avg_Age']).copy()
        temp_doctors['injury_diff'] = np.abs(temp_doctors['Tot_Benes'] - club_total_injuries)
        temp_doctors['age_diff'] = np.abs(temp_doctors['Bene_Avg_Age'] - club_average_age)

        temp_doctors['injury_diff'] = temp_doctors['injury_diff'] / (temp_doctors['injury_diff'].max() + 1e-6)
        temp_doctors['age_diff'] = temp_doctors['age_diff'] / (temp_doctors['age_diff'].max() + 1e-6)

        temp_doctors['similarity_score'] = 1 - (temp_doctors['injury_diff'] + temp_doctors['age_diff']) / 2

        return temp_doctors.sort_values(by='similarity_score', ascending=False).head(top_n)[[
            'Rndrng_Prvdr_First_Name', 'Rndrng_Prvdr_Last_Org_Name', 'Rndrng_Prvdr_Type', 'similarity_score'
        ]]

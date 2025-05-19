import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler

class PositionRecommender:
    def __init__(self, dataset_path="clubs_n.csv"):
        self.position_features = {
            "GK": ["goals_conceded", "clean_sheets"],
            "CB": ["conceded_attacks_middle"],
            "RB": ["conceded_attacks_left"],
            "LB": ["conceded_attacks_right"],
            "DMF": ["conceded_attacks_middle", "possession(%)"],
            "CM": ["pass_accuracy (%)", "possession(%)"],
            "AMF": ["shots_per_match", "goals_scored"],
            "RW": ["total_attacks_left"],
            "LW": ["total_attacks_right"],
            "ST": ["goals_scored"],
            "Coach": ["wins", "draws", "losses", "goal_difference", "ranking"],
            "Medical Staff": ["total_injuries"],
        }

        # Load dataset and scaler
        self.df = pd.read_csv(dataset_path)
        self.scaler = joblib.load("scaler.pkl")

        # Preprocessing: drop unused and rename
        drop_cols = ['total_market_value', 'coach_name', 'club_standardized_y', 'url', 'filename']
        self.df.drop(columns=[col for col in drop_cols if col in self.df.columns], inplace=True, errors='ignore')
        if 'id' in self.df.columns:
            self.df.rename(columns={'id': 'ranking'}, inplace=True)

        # Ensure all numeric columns are scaled at runtime
        self.numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    def score_positions(self, df: pd.DataFrame):
        df = df.copy()
        for position, features in self.position_features.items():
            df[f"{position}_Score"] = df[features].mean(axis=1) * 100
        return df
    def predict(self, club_name: str) -> dict:
        # Find the club row
        match = self.df[self.df["club"].str.lower() == club_name.lower()]
        if match.empty:
            raise ValueError(f"Club '{club_name}' not found in dataset.")

        row = match.iloc[0:1].copy()

        # Impute missing values if any
        row['average_age'] = row['average_age'].fillna(self.df['average_age'].mean())
        row['foreigners_percentage'] = row['foreigners_percentage'].fillna(self.df['foreigners_percentage'].mean())
        row.fillna(self.df.median(numeric_only=True), inplace=True)

        # Apply MinMaxScaler to numeric columns
        row[self.numeric_cols] = self.scaler.transform(row[self.numeric_cols])

        # Score and return top 5 weakest positions
        scored = self.score_positions(row)
        scores = {pos: scored.iloc[0][f"{pos}_Score"] for pos in self.position_features}
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])

        # Return top 5
        top_5_weakest = [pos for pos, _ in sorted_scores[:5]]

        return {
            "club": match.iloc[0]["club"],
            "top_5_weakest_positions": top_5_weakest
        }

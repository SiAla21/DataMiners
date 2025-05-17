import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load the full training data
df = pd.read_csv("clubs_n.csv")

# Drop irrelevant columns
DROP_COLS = ['total_market_value', 'coach_name', 'club_standardized_y', 'url', 'filename']
df = df.drop(columns=[col for col in DROP_COLS if col in df.columns], errors='ignore')

# Rename 'id' to 'ranking' if it exists
if 'id' in df.columns:
    df.rename(columns={'id': 'ranking'}, inplace=True)


# Impute missing values (simple logic to match Flask)
df['average_age'] = df['average_age'].fillna(df['average_age'].mean())
df['foreigners_percentage'] = df['foreigners_percentage'].fillna(df['foreigners_percentage'].mean())
df = df.fillna(df.median(numeric_only=True))

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
# Apply Min-Max Scaling
scaler = MinMaxScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

print("Min-Max Normalization Applied.")

# Save the scaler to disk
joblib.dump(scaler, 'scaler.pkl')
print("✅ scaler.pkl has been generated and saved using only model features.")

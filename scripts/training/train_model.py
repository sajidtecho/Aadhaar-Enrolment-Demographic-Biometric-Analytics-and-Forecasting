import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load processed data
df = pd.read_csv(
    r"C:\Users\Shakil Ahmad\OneDrive\Desktop\UIDAI\Adhar_biometric\01_data\processed\clean_biometric_data.csv"
)

FEATURES = [
    'bio_age_5_17',
    'bio_age_17_',
    'bio_total',
    'ratio_17_to_5'
]

X = df[FEATURES].fillna(0)
y = df['anomaly_flag'].astype(int)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight='balanced'
)

model.fit(X, y)

# Save model
joblib.dump(model, "uidai_anomaly_model.pkl")

print("✅ Supervised anomaly model trained successfully")

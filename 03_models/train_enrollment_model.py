import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "01_data", "processed", "merged_clean_aadhaar_enrolment_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "03_models", "uidai_enrollment_model.pkl")

def train_enrollment_model():
    print(f"[INFO] Loading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] Data file not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Preprocessing
    print("[INFO] Preprocessing data...")
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year_month'] = df['date'].dt.to_period('M').astype(str)
    
    # Target: age_18_greater
    # Features: age_0_5, age_5_17, and historical lags of age_18_greater
    
    # Aggregation - Group by Month-State-District
    # We aggregate to monthly level for stability
    df_agg = df.groupby(['year_month', 'state', 'district'], as_index=False)[[
        'age_0_5', 'age_5_17', 'age_18_greater'
    ]].sum()
    
    df_agg.sort_values(by=['state', 'district', 'year_month'], inplace=True)
    
    # Feature Engineering
    # 1. Date Features
    df_agg['year'] = pd.to_datetime(df_agg['year_month']).dt.year
    df_agg['month'] = pd.to_datetime(df_agg['year_month']).dt.month
    
    # 2. Location Encoding
    df_agg['state_code'] = df_agg['state'].astype('category').cat.codes
    df_agg['district_code'] = df_agg['district'].astype('category').cat.codes
    
    # 3. Ratio Features (Correlation with target)
    df_agg['total_load'] = df_agg['age_0_5'] + df_agg['age_5_17'] + df_agg['age_18_greater']
    df_agg['ratio_child'] = df_agg['age_0_5'] / (df_agg['total_load'] + 1)
    df_agg['ratio_youth'] = df_agg['age_5_17'] / (df_agg['total_load'] + 1)

    # 4. Lags (The most predictive features)
    df_agg['lag_1m_adult'] = df_agg.groupby(['state', 'district'])['age_18_greater'].shift(1).fillna(0)
    df_agg['lag_2m_adult'] = df_agg.groupby(['state', 'district'])['age_18_greater'].shift(2).fillna(0)
    df_agg['lag_3m_adult'] = df_agg.groupby(['state', 'district'])['age_18_greater'].shift(3).fillna(0)
    
    df_agg['rolling_mean_3m'] = df_agg.groupby(['state', 'district'])['age_18_greater'].rolling(window=3).mean().reset_index(level=[0,1], drop=True).fillna(0)

    # Target: Next Month's Adult Enrollment
    df_agg['target_next_month'] = df_agg.groupby(['state', 'district'])['age_18_greater'].shift(-1)
    
    # Drop rows without target
    ml_df = df_agg.dropna(subset=['target_next_month'])
    
    feature_cols = [
        'age_0_5', 'age_5_17', 
        'ratio_child', 'ratio_youth',
        'lag_1m_adult', 'lag_2m_adult', 'lag_3m_adult', 'rolling_mean_3m',
        'year', 'month', 'state_code', 'district_code'
    ]
    
    X = ml_df[feature_cols]
    y = ml_df['target_next_month']
    
    print(f"[INFO] Training Enrollment Model (RandomForest) on {len(X)} records...")
    
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X, y)
    
    # Save Model
    joblib.dump(model, MODEL_PATH)
    print(f"[INFO] Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_enrollment_model()

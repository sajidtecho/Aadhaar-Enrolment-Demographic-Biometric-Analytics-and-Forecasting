import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "01_data", "processed", "merged_clean_aadhaar_enrolment_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "03_models", "uidai_demand_model.pkl")

def train_demand_model():
    print(f"[INFO] Loading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] Data file not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Preprocessing
    print("[INFO] Preprocessing data...")
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce') # Handle potential format issues
        df['year_month'] = df['date'].dt.to_period('M').astype(str)
        
    # Map Enrollment Data to Model Features
    # age_5_17 -> bio_age_5_17
    # age_18_greater -> bio_age_17_
    
    if 'age_5_17' in df.columns:
        df.rename(columns={
            'age_5_17': 'bio_age_5_17',
            'age_18_greater': 'bio_age_17_'
        }, inplace=True)
    
    # Ensure bio_total exists (Sum of inputs used in PredictionRequest)
    # Note: Backend predict_single uses bio_age_5_17 + bio_age_17_ for bio_total
    df['bio_total'] = df['bio_age_5_17'] + df['bio_age_17_']

    # Filter out invalid rows
    df = df.dropna(subset=['bio_total', 'year_month', 'state', 'district'])

    # Aggregation - Group by Month-State-District
    print("[INFO] Aggregating data...")
    df_agg = df.groupby(['year_month', 'state', 'district'], as_index=False)[[
        'bio_age_5_17', 'bio_age_17_', 'bio_total'
    ]].sum()

    # Feature Engineering
    print("[INFO] Engineering features...")
    df_agg['signal_transition_pressure'] = df_agg['bio_age_17_'] / (df_agg['bio_total'] + 1)
    df_agg['signal_child_share'] = df_agg['bio_age_5_17'] / (df_agg['bio_total'] + 1)
    
    df_agg.sort_values(by=['state', 'district', 'year_month'], inplace=True)
    df_agg['signal_bio_growth'] = df_agg.groupby(['state', 'district'])['bio_total'].pct_change().fillna(0)
    # Fix rolling window warning or error by resetting index for rolling
    df_agg['signal_bio_volatility'] = df_agg.groupby(['state', 'district'])['bio_total'].rolling(window=3).std().reset_index(level=[0,1], drop=True).fillna(0)
    
    # Feature Selection & Encoding
    features_df = df_agg.copy()
    features_df['year'] = pd.to_datetime(features_df['year_month']).dt.year
    features_df['month'] = pd.to_datetime(features_df['year_month']).dt.month
    
    features_df['state_code'] = features_df['state'].astype('category').cat.codes
    features_df['district_code'] = features_df['district'].astype('category').cat.codes
    
    features_df['feat_bio_dependency'] = features_df['bio_total'] / (features_df['bio_age_5_17'] + 1)
    features_df['feat_lifecycle_imbalance'] = features_df['bio_age_17_'] - features_df['bio_age_5_17']
    
    features_df.sort_values(by=['state', 'district', 'year', 'month'], inplace=True)
    features_df['feat_3m_momentum'] = features_df.groupby(['state', 'district'])['bio_total'].rolling(window=3).mean().reset_index(level=[0,1], drop=True).fillna(0)
    
    # Lag Features for improved MAE
    features_df['lag_1m_bio'] = features_df.groupby(['state', 'district'])['bio_total'].shift(1).fillna(0)
    features_df['lag_2m_bio'] = features_df.groupby(['state', 'district'])['bio_total'].shift(2).fillna(0)
    features_df['lag_3m_bio'] = features_df.groupby(['state', 'district'])['bio_total'].shift(3).fillna(0)
    features_df['rolling_std_3m'] = features_df.groupby(['state', 'district'])['bio_total'].rolling(window=3).std().reset_index(level=[0,1], drop=True).fillna(0)

    # Clean infinite values or nans resulting from division/change
    features_df.replace([np.inf, -np.inf], 0, inplace=True)
    features_df.fillna(0, inplace=True)

    # Prepare Training Data
    ml_df = features_df.copy()
    ml_df['target_bio_next_month'] = ml_df.groupby(['state', 'district'])['bio_total'].shift(-1)
    
    ml_df = ml_df.dropna(subset=['target_bio_next_month'])
    
    feature_cols = [
        'bio_age_5_17', 'bio_age_17_', 'signal_transition_pressure', 'signal_child_share', 
        'signal_bio_growth', 'signal_bio_volatility', 'feat_bio_dependency', 
        'feat_lifecycle_imbalance', 'feat_3m_momentum', 
        'lag_1m_bio', 'lag_2m_bio', 'lag_3m_bio', 'rolling_std_3m',
        'year', 'month', 'state_code', 'district_code'
    ]
    
    X = ml_df[feature_cols]
    y = ml_df['target_bio_next_month']
    
    print(f"[INFO] Training Gradient Boosting Regressor on {len(X)} records...")
    model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=6,
        min_samples_leaf=5,
        random_state=42
    )
    model.fit(X, y)
    
    # Save Model
    joblib.dump(model, MODEL_PATH)
    print(f"[INFO] Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_demand_model()

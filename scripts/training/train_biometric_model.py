import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, mean_absolute_percentage_error
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIOMETRIC_DATA_PATH = os.path.join(BASE_DIR, "01_data", "processed", "clean_biometric_data.csv")
ENROLLMENT_DATA_PATH = os.path.join(BASE_DIR, "01_data", "processed", "merged_clean_aadhaar_enrolment_data.csv")
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, "03_models", "uidai_biometric_model.pkl")

def train_biometric_model():
    print("Loading data...")
    try:
        df_bio = pd.read_csv(BIOMETRIC_DATA_PATH)
        df_enrol = pd.read_csv(ENROLLMENT_DATA_PATH)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Standardize Dates
    df_bio['date'] = pd.to_datetime(df_bio['date'], errors='coerce')
    df_enrol['date'] = pd.to_datetime(df_enrol['date'], format='mixed', errors='coerce')

    # Aggregate to District-Daily level to ensure uniqueness for merge
    # Biometric: Sum numeric cols
    bio_cols = ['bio_age_5_17', 'bio_age_17_', 'bio_total']
    df_bio_agg = df_bio.groupby(['date', 'state', 'district'])[bio_cols].sum().reset_index()

    # Enrollment: Sum numeric cols
    enrol_cols = ['age_0_5', 'age_5_17', 'age_18_greater']
    df_enrol_agg = df_enrol.groupby(['date', 'state', 'district'])[enrol_cols].sum().reset_index()

    print("Merging datasets...")
    # Merge on Date, State, District
    df = pd.merge(df_bio_agg, df_enrol_agg, on=['date', 'state', 'district'], how='inner')
    
    if df.empty:
        print("Merged dataframe is empty! Check date formats or overlap.")
        return

    print(f"Merged Data Shape: {df.shape}")

    # Feature Engineering
    print("Creating enhanced features...")
    
    # Basic temporal features
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['day_of_month'] = df['date'].dt.day
    
    # Sort by date for lag features
    df = df.sort_values(['state', 'district', 'date']).reset_index(drop=True)
    
    # Lag features (1, 7, 30 days)
    print("  - Adding lag features...")
    df['bio_total_lag_1'] = df.groupby(['state', 'district'])['bio_total'].shift(1)
    df['bio_total_lag_7'] = df.groupby(['state', 'district'])['bio_total'].shift(7)
    df['bio_total_lag_30'] = df.groupby(['state', 'district'])['bio_total'].shift(30)
    
    # Rolling statistics (7-day window)
    print("  - Adding rolling statistics...")
    df['bio_total_rolling_mean_7'] = df.groupby(['state', 'district'])['bio_total'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    df['bio_total_rolling_std_7'] = df.groupby(['state', 'district'])['bio_total'].transform(
        lambda x: x.rolling(window=7, min_periods=1).std()
    )
    
    # Age ratios
    print("  - Adding age ratios...")
    df['ratio_5_17'] = df['bio_age_5_17'] / (df['bio_total'] + 1)
    df['ratio_17_plus'] = df['bio_age_17_'] / (df['bio_total'] + 1)
    
    # Interaction features
    print("  - Adding interaction features...")
    df['age_month_interaction'] = df['age_5_17'] * df['month']
    
    # Fill NaN values from lag and rolling features
    df = df.fillna(0)
    
    # Define feature columns
    features = [
        'age_0_5', 'age_5_17', 'age_18_greater',
        'month', 'day_of_week', 'quarter', 'is_weekend', 'day_of_month',
        'bio_total_lag_1', 'bio_total_lag_7', 'bio_total_lag_30',
        'bio_total_rolling_mean_7', 'bio_total_rolling_std_7',
        'ratio_5_17', 'ratio_17_plus',
        'age_month_interaction'
    ]
    target = 'bio_total'
    
    print(f"Total features created: {len(features)}")

    X = df[features]
    y = df[target]

    # Handle missing values if any
    X = X.fillna(0)
    y = y.fillna(0)

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\nTrain/Test Split:")
    print(f"  Training samples: {len(X_train):,}")
    print(f"  Testing samples:  {len(X_test):,}")

    print("\nTraining XGBoost Regressor with enhanced configuration...")
    model = XGBRegressor(
        n_estimators=200,          # More trees
        max_depth=8,               # Control overfitting
        learning_rate=0.05,        # Slower, more accurate
        subsample=0.8,             # Prevent overfitting
        colsample_bytree=0.8,      # Feature sampling
        random_state=42,
        n_jobs=-1,
        verbosity=0                # Suppress warnings
    )
    
    # Train with early stopping
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )

    # Evaluation
    print("\n" + "="*70)
    print("  MODEL EVALUATION METRICS")
    print("="*70)
    
    # Training set predictions
    y_pred_train = model.predict(X_train)
    train_mae = mean_absolute_error(y_train, y_pred_train)
    train_r2 = r2_score(y_train, y_pred_train)
    
    # Test set predictions
    y_pred_test = model.predict(X_test)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_mse = mean_squared_error(y_test, y_pred_test)
    test_rmse = np.sqrt(test_mse)
    test_r2 = r2_score(y_test, y_pred_test)
    
    # MAPE (only for non-zero actuals)
    mask = y_test > 0
    test_mape = mean_absolute_percentage_error(y_test[mask], y_pred_test[mask]) * 100 if mask.sum() > 0 else 0
    
    print(f"\nTraining Set:")
    print(f"  MAE:  {train_mae:.2f}")
    print(f"  R²:   {train_r2:.4f} ({train_r2*100:.2f}%)")
    
    print(f"\nTesting Set:")
    print(f"  MAE:  {test_mae:.2f}")
    print(f"  RMSE: {test_rmse:.2f}")
    print(f"  R²:   {test_r2:.4f} ({test_r2*100:.2f}%)")
    print(f"  MAPE: {test_mape:.2f}%")
    
    # Feature importance
    print(f"\nTop 10 Feature Importances:")
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(10).iterrows():
        print(f"  {row['feature']:<30} {row['importance']:.4f}")

    # Save Model
    print(f"\n" + "="*70)
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"Model saved to: {MODEL_OUTPUT_PATH}")
    
    # Save feature info and metrics
    model_info = {
        'model_type': 'XGBRegressor',
        'feature_columns': features,
        'n_features': len(features),
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'test_mae': float(test_mae),
        'test_rmse': float(test_rmse),
        'test_r2': float(test_r2),
        'test_mape': float(test_mape),
        'train_r2': float(train_r2),
        'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    info_path = os.path.join(BASE_DIR, "03_models", "uidai_biometric_model_info.pkl")
    joblib.dump(model_info, info_path)
    print(f"Model info saved to: {info_path}")
    
    # Save feature importance
    importance_path = os.path.join(BASE_DIR, "03_models", "biometric_feature_importance.csv")
    feature_importance.to_csv(importance_path, index=False)
    print(f"Feature importance saved to: {importance_path}")
    
    print("="*70)
    print("  BIOMETRIC MODEL TRAINING COMPLETE")
    print("="*70)

if __name__ == "__main__":
    train_biometric_model()

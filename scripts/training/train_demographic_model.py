"""
Train ML Model for Demographic Predictions
Uses RandomForestRegressor to predict demographic enrollment demand
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("  DEMOGRAPHIC MODEL TRAINING")
print("="*70)

# Load data
DATA_PATH = Path("../01_data/processed/clean_demographic_data.csv")
print(f"\n📂 Loading data from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
print(f"   ✓ Loaded {len(df):,} records")

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Feature Engineering
print(f"\n🔧 Feature Engineering:")

# Time-based features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['quarter'] = df['date'].dt.quarter
print(f"   ✓ Created time-based features")

# Target variable: total demographic demand
df['target'] = df['demo_age_5_17'] + df['demo_age_17_']

# Create aggregated features by state-district-month
print(f"   🔄 Creating aggregated features...")
monthly_agg = df.groupby(['state_encoded', 'district_encoded', 'year', 'month']).agg({
    'demo_age_5_17': ['mean', 'sum', 'std'],
    'demo_age_17_': ['mean', 'sum', 'std'],
    'target': ['mean', 'sum', 'count']
}).reset_index()

# Flatten column names
monthly_agg.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                       for col in monthly_agg.columns.values]

print(f"   ✓ Aggregated to {len(monthly_agg):,} monthly records")

# Fill NaN in std columns (from single-value groups)
for col in monthly_agg.columns:
    if 'std' in col:
        monthly_agg[col] = monthly_agg[col].fillna(0)

# Create lag features (previous month data)
print(f"   🔄 Creating lag features...")
monthly_agg = monthly_agg.sort_values(['state_encoded', 'district_encoded', 'year', 'month'])

for lag in [1, 2, 3]:
    monthly_agg[f'target_lag_{lag}'] = monthly_agg.groupby(
        ['state_encoded', 'district_encoded'])['target_mean'].shift(lag)
    monthly_agg[f'age_5_17_lag_{lag}'] = monthly_agg.groupby(
        ['state_encoded', 'district_encoded'])['demo_age_5_17_mean'].shift(lag)
    monthly_agg[f'age_17_lag_{lag}'] = monthly_agg.groupby(
        ['state_encoded', 'district_encoded'])['demo_age_17__mean'].shift(lag)

print(f"   ✓ Created lag features (1, 2, 3 months)")

# Drop rows with NaN (from lag features)
monthly_agg = monthly_agg.dropna()
print(f"   ✓ Final dataset: {len(monthly_agg):,} records after removing NaN")

# Select features for training
feature_cols = [
    'state_encoded', 'district_encoded', 'year', 'month',
    'demo_age_5_17_mean', 'demo_age_5_17_sum', 'demo_age_5_17_std',
    'demo_age_17__mean', 'demo_age_17__sum', 'demo_age_17__std',
    'target_count',
    'target_lag_1', 'target_lag_2', 'target_lag_3',
    'age_5_17_lag_1', 'age_5_17_lag_2', 'age_5_17_lag_3',
    'age_17_lag_1', 'age_17_lag_2', 'age_17_lag_3'
]

X = monthly_agg[feature_cols]
y = monthly_agg['target_mean']

print(f"\n📊 Training Data:")
print(f"   Features: {len(feature_cols)}")
print(f"   Samples: {len(X):,}")
print(f"   Feature names: {feature_cols[:5]}... (showing first 5)")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n✂️  Train-Test Split:")
print(f"   Training: {len(X_train):,} samples")
print(f"   Testing:  {len(X_test):,} samples")

# Train model
print(f"\n🤖 Training RandomForest Regressor...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1,
    verbose=0
)

model.fit(X_train, y_train)
print(f"   ✓ Model trained successfully!")

# Evaluate
print(f"\n📈 Model Evaluation:")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_mae = mean_absolute_error(y_train, y_pred_train)
train_r2 = r2_score(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)
test_r2 = r2_score(y_test, y_pred_test)

print(f"   Training Set:")
print(f"      MAE: {train_mae:.2f}")
print(f"      R²:  {train_r2:.4f}")
print(f"   Testing Set:")
print(f"      MAE: {test_mae:.2f}")
print(f"      R²:  {test_r2:.4f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n🎯 Top 5 Feature Importances:")
for idx, row in feature_importance.head(5).iterrows():
    print(f"   {row['feature']}: {row['importance']:.4f}")

# Save model
MODEL_PATH = Path("uidai_demographic_model.pkl")
joblib.dump(model, MODEL_PATH)
print(f"\n💾 Model saved to: {MODEL_PATH}")
print(f"   File size: {MODEL_PATH.stat().st_size / (1024*1024):.2f} MB")

# Save feature names for inference
feature_info = {
    'feature_columns': feature_cols,
    'model_type': 'RandomForestRegressor',
    'target': 'demographic_demand_mean',
    'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
    'training_samples': len(X_train),
    'test_mae': float(test_mae),
    'test_r2': float(test_r2)
}
joblib.dump(feature_info, 'uidai_demographic_model_info.pkl')
print(f"   ✓ Feature info saved")

print(f"\n{'='*70}")
print(f"  ✅ DEMOGRAPHIC MODEL TRAINING COMPLETE")
print(f"{'='*70}\n")

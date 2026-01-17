"""
Demographic Data Processing Script
Merges and cleans all demographic CSV files
"""
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("  DEMOGRAPHIC DATA PROCESSING")
print("="*70)

# Paths
RAW_DIR = Path("01_data/raw/Demographic")
PROCESSED_DIR = Path("01_data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load all demographic files
demographic_files = list(RAW_DIR.glob("api_data_aadhar_demographic_*.csv"))
print(f"\n📁 Found {len(demographic_files)} demographic files")

dfs = []
total_records = 0
for file in sorted(demographic_files):
    df = pd.read_csv(file)
    records = len(df)
    total_records += records
    print(f"   ✓ {file.name}: {records:,} records")
    dfs.append(df)

# Merge all dataframes
print(f"\n🔄 Merging {total_records:,} total records...")
demographic_df = pd.concat(dfs, ignore_index=True)
print(f"   ✓ Merged dataframe shape: {demographic_df.shape}")

# Display initial info
print(f"\n📊 Initial Data Info:")
print(f"   Columns: {list(demographic_df.columns)}")
print(f"   Data types:\n{demographic_df.dtypes}")
print(f"\n   First few rows:")
print(demographic_df.head())

# Data Cleaning
print(f"\n🧹 Data Cleaning:")

# 1. Convert date to datetime
demographic_df['date'] = pd.to_datetime(demographic_df['date'], format='%d-%m-%Y')
print(f"   ✓ Converted date column to datetime")

# 2. Extract time features
demographic_df['year'] = demographic_df['date'].dt.year
demographic_df['month'] = demographic_df['date'].dt.month
demographic_df['day'] = demographic_df['date'].dt.day
print(f"   ✓ Extracted year, month, day")

# 3. Check for missing values
missing = demographic_df.isnull().sum()
print(f"\n   Missing values:")
print(missing[missing > 0] if missing.sum() > 0 else "   No missing values found")

# 4. Remove duplicates
initial_count = len(demographic_df)
demographic_df = demographic_df.drop_duplicates()
duplicates_removed = initial_count - len(demographic_df)
print(f"   ✓ Removed {duplicates_removed:,} duplicate records")

# 5. Handle negative values
for col in ['demo_age_5_17', 'demo_age_17_']:
    negative_count = (demographic_df[col] < 0).sum()
    if negative_count > 0:
        print(f"   ⚠️  Found {negative_count} negative values in {col}, setting to 0")
        demographic_df.loc[demographic_df[col] < 0, col] = 0

# 6. Create total demographic column
demographic_df['total_demographic'] = demographic_df['demo_age_5_17'] + demographic_df['demo_age_17_']
print(f"   ✓ Created total_demographic column")

# 7. Encode categorical variables
from sklearn.preprocessing import LabelEncoder

le_state = LabelEncoder()
le_district = LabelEncoder()

demographic_df['state_encoded'] = le_state.fit_transform(demographic_df['state'])
demographic_df['district_encoded'] = le_district.fit_transform(demographic_df['district'])
print(f"   ✓ Encoded state and district columns")

# Statistics
print(f"\n📈 Data Statistics:")
print(demographic_df[['demo_age_5_17', 'demo_age_17_', 'total_demographic']].describe())

print(f"\n🌍 Geographic Coverage:")
print(f"   Unique states: {demographic_df['state'].nunique()}")
print(f"   Unique districts: {demographic_df['district'].nunique()}")
print(f"   Unique pincodes: {demographic_df['pincode'].nunique()}")

print(f"\n📅 Date Range:")
print(f"   From: {demographic_df['date'].min().strftime('%d-%m-%Y')}")
print(f"   To:   {demographic_df['date'].max().strftime('%d-%m-%Y')}")

# Save processed data
output_file = PROCESSED_DIR / "clean_demographic_data.csv"
demographic_df.to_csv(output_file, index=False)
print(f"\n💾 Saved processed data to: {output_file}")
print(f"   Final shape: {demographic_df.shape}")
print(f"   File size: {output_file.stat().st_size / (1024*1024):.2f} MB")

# Save label encoders for later use
import pickle
encoder_file = PROCESSED_DIR / "demographic_label_encoders.pkl"
with open(encoder_file, 'wb') as f:
    pickle.dump({'state': le_state, 'district': le_district}, f)
print(f"   ✓ Saved label encoders to: {encoder_file}")

print(f"\n{'='*70}")
print(f"  ✅ DEMOGRAPHIC DATA PROCESSING COMPLETE")
print(f"{'='*70}\n")

"""
Comprehensive Visualization Generator for Aadhaar Analytics
Generates heatmaps, lifecycle charts, and trends from all three datasets
Saves visualizations in 04_visuals folder structure
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Define paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "01_data" / "processed"
VISUALS_DIR = BASE_DIR / "04_visuals"

# Create subdirectories if they don't exist
(VISUALS_DIR / "heatmaps").mkdir(parents=True, exist_ok=True)
(VISUALS_DIR / "lifecycle").mkdir(parents=True, exist_ok=True)
(VISUALS_DIR / "trends").mkdir(parents=True, exist_ok=True)
(VISUALS_DIR / "anomalies").mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("AADHAAR ANALYTICS - COMPREHENSIVE VISUALIZATION GENERATOR")
print("=" * 80)

# ============================================================================
# LOAD DATASETS
# ============================================================================
print("\n[1/4] Loading datasets...")

# Load Biometric Data
biometric_df = pd.read_csv(DATA_DIR / "clean_biometric_data.csv")
biometric_df['date'] = pd.to_datetime(biometric_df['date'])
biometric_df['year_month'] = biometric_df['date'].dt.to_period('M')
print(f"✓ Biometric data loaded: {len(biometric_df):,} records")

# Load Enrollment Data
enrollment_df = pd.read_csv(DATA_DIR / "merged_clean_aadhaar_enrolment_data.csv")
enrollment_df['date'] = pd.to_datetime(enrollment_df['date'], format='%d-%m-%Y')
enrollment_df['year_month'] = enrollment_df['date'].dt.to_period('M')
print(f"✓ Enrollment data loaded: {len(enrollment_df):,} records")

# Load Demographic Data
demographic_df = pd.read_csv(DATA_DIR / "clean_demographic_data.csv")
demographic_df['date'] = pd.to_datetime(demographic_df['date'])
demographic_df['year_month'] = demographic_df['date'].dt.to_period('M')
print(f"✓ Demographic data loaded: {len(demographic_df):,} records")

# ============================================================================
# GENERATE HEATMAPS
# ============================================================================
print("\n[2/4] Generating heatmaps...")

# 1. Biometric Activity Heatmap (State x Month)
print("  • Creating biometric state-month heatmap...")
biometric_monthly = biometric_df.groupby(['state', 'year_month']).size().reset_index(name='count')
biometric_pivot = biometric_monthly.pivot_table(
    index='state', 
    columns='year_month', 
    values='count', 
    fill_value=0
)

plt.figure(figsize=(16, 12))
sns.heatmap(biometric_pivot, cmap='YlOrRd', linewidths=0.5, cbar_kws={'label': 'Biometric Updates'})
plt.title('Biometric Updates Heatmap - State vs Month', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('State', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(VISUALS_DIR / "heatmaps" / "biometric_state_month_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()

# 2. Enrollment Activity Heatmap (State x Month)
print("  • Creating enrollment state-month heatmap...")
enrollment_monthly = enrollment_df.groupby(['state', 'year_month']).size().reset_index(name='count')
enrollment_pivot = enrollment_monthly.pivot_table(
    index='state',
    columns='year_month',
    values='count',
    fill_value=0
)

plt.figure(figsize=(16, 12))
sns.heatmap(enrollment_pivot, cmap='Blues', linewidths=0.5, cbar_kws={'label': 'Enrollments'})
plt.title('Enrollment Activity Heatmap - State vs Month', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('State', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(VISUALS_DIR / "heatmaps" / "enrollment_state_month_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()

# 3. Demographic Activity Heatmap (State x Month)
print("  • Creating demographic state-month heatmap...")
demographic_monthly = demographic_df.groupby(['state', 'year_month']).size().reset_index(name='count')
demographic_pivot = demographic_monthly.pivot_table(
    index='state',
    columns='year_month',
    values='count',
    fill_value=0
)

plt.figure(figsize=(16, 12))
sns.heatmap(demographic_pivot, cmap='Greens', linewidths=0.5, cbar_kws={'label': 'Updates'})
plt.title('Demographic Updates Heatmap - State vs Month', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('State', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(VISUALS_DIR / "heatmaps" / "demographic_state_month_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()

# 4. Age Group Heatmap (Biometric)
print("  • Creating biometric age group heatmap...")
age_cols_bio = ['bio_age_5_17', 'bio_age_17_']
if all(col in biometric_df.columns for col in age_cols_bio):
    biometric_age_monthly = biometric_df.groupby('year_month')[age_cols_bio].sum()

    plt.figure(figsize=(14, 6))
    sns.heatmap(biometric_age_monthly.T, cmap='viridis', linewidths=0.5, 
                cbar_kws={'label': 'Count'}, annot=False)
    plt.title('Biometric Age Group Distribution - Monthly', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Age Group', fontsize=12)
    plt.yticks([0.5, 1.5], ['5-17 years', '17+ years'], rotation=0)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / "heatmaps" / "biometric_age_distribution_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()

# 5. District Activity Heatmap (Top 20 Districts)
print("  • Creating top districts heatmap...")
top_districts = biometric_df['district'].value_counts().head(20).index
district_monthly = biometric_df[biometric_df['district'].isin(top_districts)].groupby(
    ['district', 'year_month']
).size().reset_index(name='count')
district_pivot = district_monthly.pivot_table(
    index='district',
    columns='year_month',
    values='count',
    fill_value=0
)

plt.figure(figsize=(14, 10))
sns.heatmap(district_pivot, cmap='RdYlGn', linewidths=0.5, cbar_kws={'label': 'Activity Count'})
plt.title('Top 20 Districts - Monthly Activity Heatmap', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('District', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(VISUALS_DIR / "heatmaps" / "top_districts_activity_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()

print(f"  ✓ Generated 5 heatmaps in {VISUALS_DIR / 'heatmaps'}")

# ============================================================================
# GENERATE LIFECYCLE CHARTS
# ============================================================================
print("\n[3/4] Generating lifecycle charts...")

# 1. Biometric Lifecycle (Daily, Weekly, Monthly Patterns)
print("  • Creating biometric lifecycle charts...")
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Daily lifecycle
biometric_df['day_of_week'] = biometric_df['date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_pattern = biometric_df.groupby('day_of_week').size().reindex(day_order)
axes[0].bar(daily_pattern.index, daily_pattern.values, color='steelblue', alpha=0.7)
axes[0].set_title('Biometric Updates - Day of Week Pattern', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Day of Week')
axes[0].set_ylabel('Total Updates')
axes[0].grid(axis='y', alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Monthly lifecycle
monthly_pattern = biometric_df.groupby('year_month').size()
axes[1].plot(monthly_pattern.index.astype(str), monthly_pattern.values, 
             marker='o', linewidth=2, markersize=6, color='darkgreen')
axes[1].fill_between(range(len(monthly_pattern)), monthly_pattern.values, alpha=0.3, color='green')
axes[1].set_title('Biometric Updates - Monthly Lifecycle', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Total Updates')
axes[1].grid(axis='y', alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

# Age group lifecycle
age_cols_enroll = ['age_0_5', 'age_5_17', 'age_18_greater']
if all(col in enrollment_df.columns for col in age_cols_enroll):
    age_lifecycle = enrollment_df.groupby('year_month')[age_cols_enroll].sum()
    for col in age_cols_enroll:
        axes[2].plot(age_lifecycle.index.astype(str), age_lifecycle[col], 
                    marker='o', linewidth=2, label=col.replace('_', ' ').title())
    axes[2].set_title('Enrollment - Age Group Lifecycle', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Month')
    axes[2].set_ylabel('Count')
    axes[2].legend()
    axes[2].grid(axis='y', alpha=0.3)
    axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(VISUALS_DIR / "lifecycle" / "biometric_lifecycle.png", dpi=300, bbox_inches='tight')
plt.close()

# 2. Enrollment Lifecycle
print("  • Creating enrollment lifecycle charts...")
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Monthly enrollment lifecycle
enrollment_monthly_pattern = enrollment_df.groupby('year_month').size()
axes[0].plot(enrollment_monthly_pattern.index.astype(str), enrollment_monthly_pattern.values,
            marker='s', linewidth=2, markersize=6, color='navy')
axes[0].fill_between(range(len(enrollment_monthly_pattern)), enrollment_monthly_pattern.values, 
                     alpha=0.3, color='blue')
axes[0].set_title('Enrollment Lifecycle - Monthly Pattern', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Enrollments')
axes[0].grid(axis='y', alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Gender distribution lifecycle
if 'gender' in enrollment_df.columns:
    gender_lifecycle = enrollment_df.groupby(['year_month', 'gender']).size().unstack(fill_value=0)
    for gender in gender_lifecycle.columns:
        axes[1].plot(gender_lifecycle.index.astype(str), gender_lifecycle[gender],
                    marker='o', linewidth=2, label=f'Gender {gender}')
    axes[1].set_title('Enrollment Lifecycle - Gender Distribution', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Count')
    axes[1].legend()
    axes[1].grid(axis='y', alpha=0.3)
    axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(VISUALS_DIR / "lifecycle" / "enrollment_lifecycle.png", dpi=300, bbox_inches='tight')
plt.close()

# 3. Demographic Lifecycle
print("  • Creating demographic lifecycle charts...")
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Monthly demographic lifecycle
demographic_monthly_pattern = demographic_df.groupby('year_month').size()
axes[0].plot(demographic_monthly_pattern.index.astype(str), demographic_monthly_pattern.values,
            marker='D', linewidth=2, markersize=6, color='purple')
axes[0].fill_between(range(len(demographic_monthly_pattern)), demographic_monthly_pattern.values,
                     alpha=0.3, color='purple')
axes[0].set_title('Demographic Updates Lifecycle - Monthly Pattern', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Updates')
axes[0].grid(axis='y', alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# State-wise lifecycle (top 10 states)
top_states = demographic_df['state'].value_counts().head(10).index
state_lifecycle = demographic_df[demographic_df['state'].isin(top_states)].groupby(
    ['year_month', 'state']
).size().unstack(fill_value=0)

for state in state_lifecycle.columns[:5]:  # Plot top 5 for readability
    axes[1].plot(state_lifecycle.index.astype(str), state_lifecycle[state],
                marker='o', linewidth=1.5, label=state)
axes[1].set_title('Demographic Lifecycle - Top 5 States', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Updates')
axes[1].legend(loc='best')
axes[1].grid(axis='y', alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(VISUALS_DIR / "lifecycle" / "demographic_lifecycle.png", dpi=300, bbox_inches='tight')
plt.close()

print(f"  ✓ Generated 3 lifecycle charts in {VISUALS_DIR / 'lifecycle'}")

# ============================================================================
# GENERATE TREND CHARTS
# ============================================================================
print("\n[4/4] Generating trend charts...")

# 1. Combined Trends (All Three Datasets)
print("  • Creating combined trends chart...")
fig, axes = plt.subplots(3, 1, figsize=(16, 12))

# Biometric trend
biometric_trend = biometric_df.groupby('year_month').size()
axes[0].plot(biometric_trend.index.astype(str), biometric_trend.values,
            marker='o', linewidth=2.5, color='red', label='Biometric Updates')
axes[0].fill_between(range(len(biometric_trend)), biometric_trend.values, alpha=0.2, color='red')
axes[0].set_title('Biometric Updates Trend Over Time', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Count', fontsize=11)
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Enrollment trend
enrollment_trend = enrollment_df.groupby('year_month').size()
axes[1].plot(enrollment_trend.index.astype(str), enrollment_trend.values,
            marker='s', linewidth=2.5, color='blue', label='Enrollments')
axes[1].fill_between(range(len(enrollment_trend)), enrollment_trend.values, alpha=0.2, color='blue')
axes[1].set_title('Enrollment Trend Over Time', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Count', fontsize=11)
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

# Demographic trend
demographic_trend = demographic_df.groupby('year_month').size()
axes[2].plot(demographic_trend.index.astype(str), demographic_trend.values,
            marker='D', linewidth=2.5, color='green', label='Demographic Updates')
axes[2].fill_between(range(len(demographic_trend)), demographic_trend.values, alpha=0.2, color='green')
axes[2].set_title('Demographic Updates Trend Over Time', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Month', fontsize=11)
axes[2].set_ylabel('Count', fontsize=11)
axes[2].legend(loc='upper left')
axes[2].grid(True, alpha=0.3)
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(VISUALS_DIR / "trends" / "combined_trends.png", dpi=300, bbox_inches='tight')
plt.close()

# 2. State-wise Trends (Top 10 States)
print("  • Creating state-wise trends...")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Biometric state trends
top_bio_states = biometric_df['state'].value_counts().head(10).index
bio_state_trends = biometric_df[biometric_df['state'].isin(top_bio_states)].groupby(
    ['year_month', 'state']
).size().unstack(fill_value=0)

for state in bio_state_trends.columns[:5]:
    axes[0].plot(bio_state_trends.index.astype(str), bio_state_trends[state], 
                marker='o', linewidth=1.5, label=state)
axes[0].set_title('Biometric - Top 5 States Trend', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Updates')
axes[0].legend(loc='best', fontsize=8)
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Enrollment state trends
top_enr_states = enrollment_df['state'].value_counts().head(10).index
enr_state_trends = enrollment_df[enrollment_df['state'].isin(top_enr_states)].groupby(
    ['year_month', 'state']
).size().unstack(fill_value=0)

for state in enr_state_trends.columns[:5]:
    axes[1].plot(enr_state_trends.index.astype(str), enr_state_trends[state],
                marker='s', linewidth=1.5, label=state)
axes[1].set_title('Enrollment - Top 5 States Trend', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Enrollments')
axes[1].legend(loc='best', fontsize=8)
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

# Demographic state trends
top_demo_states = demographic_df['state'].value_counts().head(10).index
demo_state_trends = demographic_df[demographic_df['state'].isin(top_demo_states)].groupby(
    ['year_month', 'state']
).size().unstack(fill_value=0)

for state in demo_state_trends.columns[:5]:
    axes[2].plot(demo_state_trends.index.astype(str), demo_state_trends[state],
                marker='D', linewidth=1.5, label=state)
axes[2].set_title('Demographic - Top 5 States Trend', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Month')
axes[2].set_ylabel('Updates')
axes[2].legend(loc='best', fontsize=8)
axes[2].grid(True, alpha=0.3)
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(VISUALS_DIR / "trends" / "state_wise_trends.png", dpi=300, bbox_inches='tight')
plt.close()

# 3. Growth Rate Trends
print("  • Creating growth rate trends...")
fig, ax = plt.subplots(figsize=(14, 6))

# Calculate month-over-month growth rates
bio_growth = biometric_trend.pct_change() * 100
enr_growth = enrollment_trend.pct_change() * 100
demo_growth = demographic_trend.pct_change() * 100

ax.plot(bio_growth.index.astype(str), bio_growth.values, 
        marker='o', linewidth=2, label='Biometric Growth %', color='red')
ax.plot(enr_growth.index.astype(str), enr_growth.values,
        marker='s', linewidth=2, label='Enrollment Growth %', color='blue')
ax.plot(demo_growth.index.astype(str), demo_growth.values,
        marker='D', linewidth=2, label='Demographic Growth %', color='green')

ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax.set_title('Month-over-Month Growth Rate Trends', fontsize=14, fontweight='bold')
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Growth Rate (%)', fontsize=11)
ax.legend(loc='best')
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(VISUALS_DIR / "trends" / "growth_rate_trends.png", dpi=300, bbox_inches='tight')
plt.close()

print(f"  ✓ Generated 3 trend charts in {VISUALS_DIR / 'trends'}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("VISUALIZATION GENERATION COMPLETE")
print("=" * 80)
print(f"\n📊 Total visualizations generated: 11")
print(f"\n📁 Output directories:")
print(f"   • Heatmaps:  {VISUALS_DIR / 'heatmaps'}  (5 files)")
print(f"   • Lifecycle: {VISUALS_DIR / 'lifecycle'} (3 files)")
print(f"   • Trends:    {VISUALS_DIR / 'trends'}    (3 files)")
print(f"\n✓ All visualizations saved successfully!")
print("=" * 80 + "\n")

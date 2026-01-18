import pandas as pd
import numpy as np
from schemas import Metric, TrendData, DistrictRisk, DashboardResponse
from model_service import model_service

class DashboardService:
    def get_dashboard_data(self) -> DashboardResponse:
        # Check if data is loaded
        if model_service.data is None or model_service.enrollment_data is None:
             raise ValueError("Operational Data Not Loaded. Cannot serve Dashboard.")

        bio_df = model_service.data
        enrol_df = model_service.enrollment_data
        
        # 1. KPIs Calculation - BIOMETRIC DATA
        # ----------------------------------------
        bio_last_month = bio_df['date'].max()
        bio_current = bio_df[bio_df['date'] == bio_last_month]
        bio_prev = bio_df[bio_df['date'] == (bio_last_month - pd.DateOffset(months=1))]
        
        # Biometric Metrics
        curr_bio = bio_current['bio_total'].sum()
        prev_bio = bio_prev['bio_total'].sum()
        bio_change = ((curr_bio - prev_bio) / prev_bio) * 100 if prev_bio > 0 else 0
        
        # High Risk Districts (using heuristic threshold)
        threshold = bio_df['bio_total'].quantile(0.95)
        high_risk_count = bio_current[bio_current['bio_total'] > threshold].shape[0]
        
        # 2. KPIs Calculation - ENROLLMENT DATA
        # ----------------------------------------
        enrol_last_month = enrol_df['date'].max()
        enrol_current = enrol_df[enrol_df['date'] == enrol_last_month]
        enrol_prev = enrol_df[enrol_df['date'] == (enrol_last_month - pd.DateOffset(months=1))]
        
        # Calculate total enrollments
        if 'age_0_5' in enrol_current.columns:
            curr_enrol = enrol_current['age_0_5'].sum() + enrol_current['age_5_17'].sum() + enrol_current['age_18_greater'].sum()
            prev_enrol = enrol_prev['age_0_5'].sum() + enrol_prev['age_5_17'].sum() + enrol_prev['age_18_greater'].sum()
        else:
            curr_enrol = enrol_current['bio_total'].sum() if 'bio_total' in enrol_current.columns else 0
            prev_enrol = enrol_prev['bio_total'].sum() if 'bio_total' in enrol_prev.columns else 0
            
        enrol_change = ((curr_enrol - prev_enrol) / prev_enrol) * 100 if prev_enrol > 0 else 0
        
        # Adult enrollments (18+)
        curr_adult = enrol_current['age_18_greater'].sum() if 'age_18_greater' in enrol_current.columns else 0
        prev_adult = enrol_prev['age_18_greater'].sum() if 'age_18_greater' in enrol_prev.columns else 0
        adult_change = ((curr_adult - prev_adult) / prev_adult) * 100 if prev_adult > 0 else 0
        
        kpi = [
            Metric(
                label='Biometric Updates (Actual)', 
                value=f"{curr_bio/1000:.1f}k", 
                change=round(bio_change, 1), 
                trend='up' if bio_change > 0 else 'down'
            ),
            Metric(
                label='Total Enrollments (Actual)', 
                value=f"{curr_enrol/1000:.1f}k", 
                change=round(enrol_change, 1), 
                trend='up' if enrol_change > 0 else 'down'
            ),
            Metric(
                label='Adult Enrollments (18+)', 
                value=f"{curr_adult/1000:.1f}k", 
                change=round(adult_change, 1), 
                trend='up' if adult_change > 0 else 'down'
            ),
            Metric(
                label='High Demand Districts', 
                value=str(high_risk_count), 
                change=round(bio_change * 0.1, 1), 
                trend='up' if bio_change > 0 else 'down'
            ),
        ]

        # 3. Trend Data (Historical + Forecast) - BIOMETRIC
        # ----------------------------------------
        bio_trend_df = bio_df.groupby('date')['bio_total'].sum().reset_index()
        bio_trend_df = bio_trend_df.sort_values('date').tail(6) # Last 6 months
        
        trend = []
        for _, row in bio_trend_df.iterrows():
            trend.append(TrendData(
                month=row['date'].strftime("%b"), 
                actual=int(row['bio_total']), 
                predicted=int(row['bio_total']), # History "prediction" matches actual
                confidenceLower=int(row['bio_total']*0.95), 
                confidenceUpper=int(row['bio_total']*1.05)
            ))
            
        # Add 1 Month Biometric Forecast
        bio_growth = bio_trend_df['bio_total'].pct_change().tail(3).mean()
        bio_last_val = bio_trend_df['bio_total'].iloc[-1]
        bio_next_val = int(bio_last_val * (1 + bio_growth))
        
        next_month_name = (bio_trend_df['date'].iloc[-1] + pd.DateOffset(months=1)).strftime("%b")
        trend.append(TrendData(
            month=next_month_name,
            actual=None,
            predicted=bio_next_val,
            confidenceLower=int(bio_next_val*0.9),
            confidenceUpper=int(bio_next_val*1.1)
        ))

        # 4. Districts Risk List (Top Districts by Biometric Volume)
        # ----------------------------------------
        top_districts = bio_current.sort_values('bio_total', ascending=False).head(5)
        
        districts = []
        for i, row in top_districts.iterrows():
            # Classify status based on volume
            status = 'Medium'
            if row['bio_total'] > threshold:
                status = 'Critical'
            elif row['bio_total'] > threshold * 0.8:
                status = 'High'
                
            districts.append(DistrictRisk(
                id=str(i),
                district=row['district'],
                state=row['state'],
                riskScore=min(99, int((row['bio_total'] / bio_trend_df['bio_total'].max()) * 100)),
                prediction=int(row['bio_total']),
                status=status
            ))

        return DashboardResponse(
            kpi=kpi,
            trend=trend,
            districts=districts
        )

    def get_full_risk_report(self) -> list[DistrictRisk]:
        """Returns risk assessment for ALL active districts in the latest month."""
        if model_service.data is None:
             return []

        df = model_service.data
        last_month = df['date'].max()
        current_data = df[df['date'] == last_month].copy()
        
        # Determine strict thresholds for anomaly detection
        threshold_critical = current_data['bio_total'].quantile(0.98)
        threshold_high = current_data['bio_total'].quantile(0.90)
        threshold_medium = current_data['bio_total'].quantile(0.75)
        max_vol = current_data['bio_total'].max()

        report = []
        for i, row in current_data.sort_values('bio_total', ascending=False).iterrows():
            vol = row['bio_total']
            
            status = 'Low'
            if vol > threshold_critical: status = 'Critical'
            elif vol > threshold_high: status = 'High'
            elif vol > threshold_medium: status = 'Medium'
            
            # Optimization: Skip 'Low' risk to ensure API responsiveness and relevance
            # Processing 20k+ records causes timeouts
            if status == 'Low':
                continue

            # Risk score 0-100 normalized against max volume
            score = int((vol / max_vol) * 100) if max_vol > 0 else 0
            
            report.append(DistrictRisk(
                id=str(i),
                district=row['district'],
                state=row['state'],
                riskScore=score,
                prediction=int(vol),
                status=status
            ))
            
        return report
    
    def get_enrollment_trends(self) -> list[TrendData]:
        """Returns enrollment trend data separately"""
        if model_service.enrollment_data is None:
            return []
            
        enrol_df = model_service.enrollment_data
        
        # Calculate total enrollments per date
        if 'age_0_5' in enrol_df.columns:
            enrol_df['total_enrol'] = enrol_df['age_0_5'] + enrol_df['age_5_17'] + enrol_df['age_18_greater']
        
        # Group by date
        enrol_trend_df = enrol_df.groupby('date')['total_enrol'].sum().reset_index()
        enrol_trend_df = enrol_trend_df.sort_values('date').tail(6)
        
        trends = []
        for _, row in enrol_trend_df.iterrows():
            trends.append(TrendData(
                month=row['date'].strftime("%b"),
                actual=int(row['total_enrol']),
                predicted=int(row['total_enrol']),
                confidenceLower=int(row['total_enrol'] * 0.95),
                confidenceUpper=int(row['total_enrol'] * 1.05)
            ))
        
        # Add forecast
        growth = enrol_trend_df['total_enrol'].pct_change().tail(3).mean()
        last_val = enrol_trend_df['total_enrol'].iloc[-1]
        next_val = int(last_val * (1 + growth))
        next_month = (enrol_trend_df['date'].iloc[-1] + pd.DateOffset(months=1)).strftime("%b")
        
        trends.append(TrendData(
            month=next_month,
            actual=None,
            predicted=next_val,
            confidenceLower=int(next_val * 0.9),
            confidenceUpper=int(next_val * 1.1)
        ))
        
        return trends

dashboard_service = DashboardService()

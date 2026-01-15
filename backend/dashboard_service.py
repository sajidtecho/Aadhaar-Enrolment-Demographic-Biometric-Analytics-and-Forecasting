import pandas as pd
import numpy as np
from .schemas import Metric, TrendData, DistrictRisk, DashboardResponse
from .model_service import model_service

class DashboardService:
    def get_dashboard_data(self) -> DashboardResponse:
        # Check if data is loaded
        if model_service.data is None:
             raise ValueError("Operational Data Not Loaded. Cannot serve Dashboard.")

        df = model_service.data
        
        # 1. KPIs Calculation
        # ----------------------------------------
        last_month = df['date'].max()
        current_month_data = df[df['date'] == last_month]
        prev_month_data = df[df['date'] == (last_month - pd.DateOffset(months=1))]
        
        # Metric: Total Biometric Demand
        curr_bio = current_month_data['bio_total'].sum()
        prev_bio = prev_month_data['bio_total'].sum()
        bio_change = ((curr_bio - prev_bio) / prev_bio) * 100 if prev_bio > 0 else 0
        
        # Metric: High Risk Districts (using heuristic threshold)
        # Using 90th percentile of bio_total as "High Traffic/Risk"
        threshold = df['bio_total'].quantile(0.95)
        high_risk_count = current_month_data[current_month_data['bio_total'] > threshold].shape[0]
        
        kpi = [
            Metric(
                label='Total Biometric Updates', 
                value=f"{curr_bio/1000:.1f}k", 
                change=round(bio_change, 1), 
                trend='up' if bio_change > 0 else 'down'
            ),
            Metric(label='Active Districts', value=str(df['district'].nunique()), change=0, trend='neutral'),
            Metric(label='State Coverage', value=str(df['state'].nunique()), change=0, trend='neutral'),
            Metric(
                label='High Demand Districts', 
                value=str(high_risk_count), 
                change=5.0, 
                trend='up'
            ),
        ]

        # 2. Trend Data (Historical + Forecast)
        # ----------------------------------------
        # Group by month for national trend
        trend_df = df.groupby('date')['bio_total'].sum().reset_index()
        trend_df = trend_df.sort_values('date').tail(6) # Last 6 months
        
        trend = []
        for _, row in trend_df.iterrows():
            trend.append(TrendData(
                month=row['date'].strftime("%b"), 
                actual=int(row['bio_total']), 
                predicted=int(row['bio_total']), # History "prediction" matches actual
                confidenceLower=int(row['bio_total']*0.95), 
                confidenceUpper=int(row['bio_total']*1.05)
            ))
            
        # Add 1 Month Forecast using simple projection (since simple agg prediction is complex)
        # For a true national forecast, we'd sum district predictions, but that's expensive for dashboard load.
        # We'll use the average growth rate of the last 3 months.
        growth_rate = trend_df['bio_total'].pct_change().tail(3).mean()
        last_val = trend_df['bio_total'].iloc[-1]
        next_val = int(last_val * (1 + growth_rate))
        
        next_month_name = (trend_df['date'].iloc[-1] + pd.DateOffset(months=1)).strftime("%b")
        trend.append(TrendData(
            month=next_month_name,
            actual=None,
            predicted=next_val,
            confidenceLower=int(next_val*0.9),
            confidenceUpper=int(next_val*1.1)
        ))

        # 3. Districts Risk List (Top Districts by Volume)
        # ----------------------------------------
        # Get top 5 districts by volume in the last month
        top_districts = current_month_data.sort_values('bio_total', ascending=False).head(5)
        
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
                riskScore=min(99, int((row['bio_total'] /  trend_df['bio_total'].max()) * 100)), # Norm score
                prediction=int(row['bio_total']), # Current volume as proxy/baseline
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

    def get_mock_fallback(self) -> DashboardResponse:
        # Keep original mock data as fallback if CSV fails to load
        kpi = [
            Metric(label='Predicted Biometric Updates', value='1.2M', change=12.5, trend='up'),
            Metric(label='Predicted Demographic Updates', value='4.5M', change=-2.3, trend='down'),
            Metric(label='Predicted Enrolments', value='850K', change=5.1, trend='up'),
            Metric(label='High-Risk Districts', value='24', change=15.0, trend='up'),
        ]
        # ... (simplified fallback)
        return DashboardResponse(kpi=kpi, trend=[], districts=[])

dashboard_service = DashboardService()

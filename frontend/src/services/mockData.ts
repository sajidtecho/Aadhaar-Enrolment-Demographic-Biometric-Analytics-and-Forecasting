export interface TrendData {
    month: string;
    actual: number | null;
    predicted: number;
    confidenceLower: number;
    confidenceUpper: number;
}

export interface Metric {
    label: string;
    value: string;
    change: number; // percentage
    trend: 'up' | 'down' | 'neutral';
}

export interface DistrictRisk {
    id: string;
    district: string;
    state: string;
    riskScore: number; // 0-100
    prediction: number;
    status: 'Critical' | 'High' | 'Medium' | 'Low';
}

export const mockDashboardData = {
    kpi: [
        { label: 'Predicted Biometric Updates', value: '1.2M', change: 12.5, trend: 'up' },
        { label: 'Predicted Demographic Updates', value: '4.5M', change: -2.3, trend: 'down' },
        { label: 'Predicted Enrolments', value: '850K', change: 5.1, trend: 'up' },
        { label: 'High-Risk Districts', value: '24', change: 15.0, trend: 'up' },
    ] as Metric[],

    trend: [
        { month: 'Jan', actual: 4200, predicted: 4150, confidenceLower: 4000, confidenceUpper: 4300 },
        { month: 'Feb', actual: 4350, predicted: 4300, confidenceLower: 4150, confidenceUpper: 4450 },
        { month: 'Mar', actual: 4480, predicted: 4500, confidenceLower: 4350, confidenceUpper: 4650 },
        { month: 'Apr', actual: 4600, predicted: 4620, confidenceLower: 4470, confidenceUpper: 4770 },
        { month: 'May', actual: 4750, predicted: 4700, confidenceLower: 4550, confidenceUpper: 4850 },
        { month: 'Jun', actual: null, predicted: 4900, confidenceLower: 4700, confidenceUpper: 5100 },
        { month: 'Jul', actual: null, predicted: 5100, confidenceLower: 4850, confidenceUpper: 5350 },
        { month: 'Aug', actual: null, predicted: 5250, confidenceLower: 4950, confidenceUpper: 5550 },
    ] as TrendData[],

    districts: [
        { id: '1', district: 'Pune', state: 'Maharashtra', riskScore: 92, prediction: 15400, status: 'Critical' },
        { id: '2', district: 'Bangalore Urban', state: 'Karnataka', riskScore: 88, prediction: 12100, status: 'Critical' },
        { id: '3', district: 'Jaipur', state: 'Rajasthan', riskScore: 85, prediction: 9800, status: 'High' },
        { id: '4', district: 'Lucknow', state: 'Uttar Pradesh', riskScore: 82, prediction: 11200, status: 'High' },
        { id: '5', district: 'Patna', state: 'Bihar', riskScore: 78, prediction: 10500, status: 'Ordering' },
    ] as DistrictRisk[]
};

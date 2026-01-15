import axios from 'axios';

// Create axios instance (ready for real backend)
const api = axios.create({
    baseURL: 'http://localhost:8002/api', // Python backend URL
    timeout: 10000,
});

export interface Metric {
    label: string;
    value: string;
    change: number; // percentage
    trend: 'up' | 'down' | 'neutral';
}

export interface TrendData {
    month: string;
    actual: number | null;
    predicted: number;
    confidenceLower: number;
    confidenceUpper: number;
}

export interface DistrictRisk {
    id: string;
    district: string;
    state: string;
    riskScore: number; // 0-100
    prediction: number;
    status: 'Critical' | 'High' | 'Medium' | 'Low';
}

export interface DashboardResponse {
    kpi: Metric[];
    trend: TrendData[];
    districts: DistrictRisk[];
}

export interface PredictionRequest {
    state: string;
    district: string;
    year: number;
    month: number;
    bio_age_5_17: number;
    bio_age_17_: number;
    prediction_type?: 'demand' | 'enrollment';
    age_0_5?: number;
}

// Real Prediction Service
export const predictDemand = async (payload: any) => {
    try {
        const response = await api.post('/predict', payload);
        return response.data;
    } catch (error: any) {
        console.error("API Call Failed:", error);
        throw error;
    }
};

export const verifyModelConnection = async (payload: any) => {
    try {
        const response = await api.post('/predict', payload);
        return {
            success: true,
            data: response.data,
            status: response.status
        };
    } catch (error: any) {
        return {
            success: false,
            error: error.message,
            status: error.response?.status || 500,
            details: error.response?.data
        };
    }
};

export const getDashboardData = async (): Promise<DashboardResponse> => {
    const response = await api.get<DashboardResponse>('/dashboard');
    return response.data;
};

export const getAnomalies = async (): Promise<DistrictRisk[]> => {
    const response = await api.get<DistrictRisk[]>('/anomalies');
    return response.data;
};

export default api;

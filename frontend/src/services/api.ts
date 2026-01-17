import axios from 'axios';

// Create axios instance (ready for real backend)
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002/api',
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

export const getEnrollmentTrends = async (): Promise<TrendData[]> => {
    const response = await api.get<{value: TrendData[], Count: number}>('/enrollment-trends');
    return response.data.value;
};

export const getAnomalies = async (): Promise<DistrictRisk[]> => {
    const response = await api.get<DistrictRisk[]>('/anomalies');
    return response.data;
};

export default api;

export interface BiometricPredictionRequest {
    age_0_5: number;
    age_5_17: number;
    age_18_greater: number;
    month: number;
    day_of_week?: number;
}

export interface BiometricPredictionResponse {
    predicted_bio_total: number;
    confidence_score: number;
}

export const predictBiometricLoad = async (data: BiometricPredictionRequest): Promise<BiometricPredictionResponse> => {
    try {
        const response = await api.post('/predict/biometric', data);
        return response.data;
    } catch (error) {
         console.error('Biometric Prediction API Error:', error);
        throw error;
    }
};

export interface DemographicPredictionResponse {
    prediction: number;
    confidence: number;
    trend: number;
    state: string;
    district: string;
}

export const predictDemographic = async (payload: PredictionRequest): Promise<DemographicPredictionResponse> => {
    try {
        const response = await api.post('/predict/demographic', payload);
        return response.data;
    } catch (error) {
        console.error('Demographic Prediction API Error:', error);
        throw error;
    }
};

import { useState } from 'react';
import PredictionForm from '../components/prediction/PredictionForm';
import PredictionResult from '../components/prediction/PredictionResult';
import { predictDemand } from '../services/api';

export default function Prediction() {
    const [result, setResult] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string|null>(null);

    const handlePredict = async (data: any) => {
        setIsLoading(true);
        setError(null);
        try {
            const res = await predictDemand(data);
            setResult(res);
        } catch (err: any) {
            console.error("Prediction failed", err);
            setError("Failed to fetch prediction. Ensure Backend is running on Port 8002.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Operational Demand Prediction</h1>
                    <p className="text-slate-500">Forecast biometric, demographic, and enrolment volumes</p>
                </div>
            </div>
            
            {error && (
                <div className="bg-red-50 text-red-700 p-4 rounded-lg border border-red-200">
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                    <PredictionForm onPredict={handlePredict} isLoading={isLoading} />
                </div>
                <div className="lg:col-span-2">
                    <PredictionResult data={result} />
                </div>
            </div>
        </div>
    );
}

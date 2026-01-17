import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import PredictionForm from '../components/prediction/PredictionForm';
import PredictionResult from '../components/prediction/PredictionResult';
import { predictDemand, predictBiometricLoad, predictDemographic } from '../services/api';
import { Download, FileText, FileSpreadsheet } from 'lucide-react';
import { exportPredictions } from '../utils/exportUtils';

export default function Prediction() {
    const { type } = useParams<{ type: string }>();
    const [result, setResult] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string|null>(null);
    const [predictionType, setPredictionType] = useState<string>('demand');
    const [showExportMenu, setShowExportMenu] = useState(false);
    
    // Set prediction type based on URL parameter
    useEffect(() => {
        if (type === 'biometric') {
            setPredictionType('biometric_load');
        } else if (type === 'demographic') {
            setPredictionType('demand');
        } else if (type === 'enrolment') {
            setPredictionType('enrollment');
        }
    }, [type]);

    const handlePredict = async (data: any) => {
        setIsLoading(true);
        setError(null);
        try {
            const horizon = parseInt(data.horizon) || 1;
            const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            
            // Generate predictions for current month + next N months based on horizon
            const predictions = [];
            let currentMonth = data.month;
            let currentYear = data.year;
            
            for (let i = 0; i < horizon; i++) {
                const predData = { ...data, month: currentMonth, year: currentYear };
                
                if (data.type === 'biometric_load') {
                    const req = {
                        age_0_5: predData.age_0_5,
                        age_5_17: predData.bio_age_5_17,
                        age_18_greater: predData.bio_age_17_,
                        month: currentMonth,
                        day_of_week: 1
                    };
                    const bioRes = await predictBiometricLoad(req);
                    predictions.push({
                        month: `${monthNames[currentMonth - 1]} ${currentYear}`,
                        value: bioRes.predicted_bio_total,
                        isPrediction: true
                    });
                } else if (data.type === 'demand') {
                    // Use demographic prediction endpoint
                    const demoRes = await predictDemographic(predData);
                    predictions.push({
                        month: `${monthNames[currentMonth - 1]} ${currentYear}`,
                        value: demoRes.prediction,
                        isPrediction: true
                    });
                } else {
                    const res = await predictDemand(predData);
                    predictions.push({
                        month: `${monthNames[currentMonth - 1]} ${currentYear}`,
                        value: res.prediction,
                        isPrediction: true
                    });
                }
                
                // Move to next month
                currentMonth++;
                if (currentMonth > 12) {
                    currentMonth = 1;
                    currentYear++;
                }
            }
            
            // Get the first prediction for main display
            let res;
            if (data.type === 'biometric_load') {
                const req = {
                    age_0_5: data.age_0_5,
                    age_5_17: data.bio_age_5_17,
                    age_18_greater: data.bio_age_17_,
                    month: data.month,
                    day_of_week: 1
                };
                const bioRes = await predictBiometricLoad(req);
                res = {
                    prediction: bioRes.predicted_bio_total,
                    confidence: bioRes.confidence_score * 100,
                    trend: 0,
                    history: [],
                    operationalMetrics: {
                        avgMonthlyLoad: bioRes.predicted_bio_total,
                        peakPressureRatio: 0,
                        persistenceScore: 0
                    },
                    predictedMonth: data.month,
                    predictedYear: data.year,
                    futurePredictions: predictions
                };
            } else if (data.type === 'demand') {
                // Use demographic prediction endpoint
                const demoRes = await predictDemographic(data);
                res = {
                    prediction: demoRes.prediction,
                    confidence: demoRes.confidence,
                    trend: demoRes.trend,
                    history: [],
                    operationalMetrics: {
                        avgMonthlyLoad: demoRes.prediction,
                        peakPressureRatio: 0,
                        persistenceScore: 0
                    },
                    predictedMonth: data.month,
                    predictedYear: data.year,
                    futurePredictions: predictions
                };
            } else {
                res = await predictDemand(data);
                res.predictedMonth = data.month;
                res.predictedYear = data.year;
                res.futurePredictions = predictions;
            }
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
                    <h1 className="text-2xl font-bold text-slate-800">
                        {type === 'biometric' && 'Biometric Operational Demand Prediction'}
                        {type === 'demographic' && 'Demographic Demand Prediction'}
                        {type === 'enrolment' && 'Enrollment Operational Forecast'}
                    </h1>
                    <p className="text-slate-500">
                        {type === 'biometric' && 'Forecast biometric processing load and capacity requirements'}
                        {type === 'demographic' && 'Forecast demographic biometric demand patterns'}
                        {type === 'enrolment' && 'Forecast enrollment trends for operational planning'}
                    </p>
                </div>
                {result && (
                    <div className="relative">
                        <button
                            onClick={() => setShowExportMenu(!showExportMenu)}
                            className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50"
                        >
                            <Download className="w-4 h-4" />
                            Export Results
                        </button>
                        {showExportMenu && (
                            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 z-10">
                                <button
                                    onClick={() => {
                                        const exportData = result.predictions?.map((p: any) => ({
                                            Month: p.month,
                                            'Predicted Value': p.value,
                                            Type: type
                                        })) || [];
                                        exportPredictions(exportData, 'csv', { type, location: result.location });
                                        setShowExportMenu(false);
                                    }}
                                    className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm text-slate-600 hover:bg-slate-50 rounded-t-lg"
                                >
                                    <FileSpreadsheet className="w-4 h-4" />
                                    Export as CSV
                                </button>
                                <button
                                    onClick={() => {
                                        const exportData = result.predictions?.map((p: any) => ({
                                            Month: p.month,
                                            'Predicted Value': p.value,
                                            Type: type
                                        })) || [];
                                        exportPredictions(exportData, 'pdf', { type, location: result.location });
                                        setShowExportMenu(false);
                                    }}
                                    className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm text-slate-600 hover:bg-slate-50"
                                >
                                    <FileText className="w-4 h-4" />
                                    Export as PDF
                                </button>
                                <button
                                    onClick={() => {
                                        const exportData = result.predictions?.map((p: any) => ({
                                            Month: p.month,
                                            'Predicted Value': p.value,
                                            Type: type
                                        })) || [];
                                        exportPredictions(exportData, 'word', { type, location: result.location });
                                        setShowExportMenu(false);
                                    }}
                                    className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm text-slate-600 hover:bg-slate-50 rounded-b-lg"
                                >
                                    <FileText className="w-4 h-4" />
                                    Export as Word
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>
            
            {error && (
                <div className="bg-red-50 text-red-700 p-4 rounded-lg border border-red-200">
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                    <PredictionForm onPredict={handlePredict} isLoading={isLoading} initialType={predictionType} />
                </div>
                <div className="lg:col-span-2">
                    <PredictionResult data={result} />
                </div>
            </div>
        </div>
    );
}

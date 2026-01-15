import { useState, useEffect } from 'react';
import FeatureImportance from '../components/insights/FeatureImportance';
import DistributionPlanModal from '../components/insights/DistributionPlanModal';
import { Lightbulb, Target, Zap, AlertTriangle, ChevronDown, Filter } from 'lucide-react';
import api from '../services/api';
import { states as allStates, districts as allDistricts } from '../utils/locations';

interface InsightsData {
    feature_importance: Array<{name: string, value: number, color: string}>;
    anomalies: Array<{district: string, severity: string, description: string}>;
    seasonal_insight: string;
    mape_score: number;
    recommendation: string;
}

export default function ModelInsights() {
    const [isPlanOpen, setIsPlanOpen] = useState(false);
    const [insights, setInsights] = useState<InsightsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Filters
    const [selectedState, setSelectedState] = useState('');
    const [selectedDistrict, setSelectedDistrict] = useState('');

    const fetchInsights = async (state?: string, district?: string) => {
        setLoading(true);
        try {
            const params: any = {};
            if (state && state !== 'All India') params.state = state;
            if (district && district !== 'All Districts') params.district = district;

            const response = await api.get('/insights', { params });
            setInsights(response.data);
            setError(null);
        } catch (err) {
            console.error("Failed to fetch insights:", err);
            setError("Failed to load model insights. Please ensure the backend is running.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchInsights();
    }, []);

    const handleApplyFilters = () => {
        fetchInsights(selectedState, selectedDistrict);
    };

    const states = ['All India', ...allStates];

    if (error) {
        return <div className="p-8 text-center text-red-500 bg-red-50 rounded-lg border border-red-200">{error}</div>;
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Model Insights</h1>
                    <p className="text-slate-500">Understanding the "Why" behind predictions</p>
                </div>
            </div>

            {/* Filter Section */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap gap-4 items-end">
                <div className="space-y-1.5 min-w-[200px]">
                    <label className="text-sm font-medium text-slate-700">State</label>
                    <div className="relative">
                        <select
                            title="Select State"
                            aria-label="Select State"
                            className="w-full pl-3 pr-8 py-2 bg-slate-50 border border-slate-200 rounded-lg appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                            value={selectedState}
                            onChange={(e) => {
                                setSelectedState(e.target.value);
                                setSelectedDistrict('');
                            }}
                        >
                            <option value="">Select State</option>
                            {states.map(s => <option key={s} value={s}>{s}</option>)}
                        </select>
                        <ChevronDown className="absolute right-3 top-2.5 w-4 h-4 text-slate-500 pointer-events-none" />
                    </div>
                </div>

                <div className="space-y-1.5 min-w-[200px]">
                    <label className="text-sm font-medium text-slate-700">District</label>
                    <div className="relative">
                        <select
                            title="Select District"
                            aria-label="Select District"
                            className="w-full pl-3 pr-8 py-2 bg-slate-50 border border-slate-200 rounded-lg appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm disabled:opacity-50"
                            value={selectedDistrict}
                            onChange={(e) => setSelectedDistrict(e.target.value)}
                            disabled={!selectedState || selectedState === 'All India'}
                        >
                            <option value="">Select District</option>
                             {selectedState && selectedState !== 'All India' && allDistricts[selectedState]?.map((d: string) => (
                                <option key={d} value={d}>{d}</option>
                            ))}
                        </select>
                        <ChevronDown className="absolute right-3 top-2.5 w-4 h-4 text-slate-500 pointer-events-none" />
                    </div>
                </div>

                <button
                    onClick={handleApplyFilters}
                    disabled={loading}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium flex items-center gap-2 disabled:opacity-50"
                >
                    <Filter className="w-4 h-4" />
                    Apply Filters
                </button>
            </div>

            {loading ? (
                <div className="p-12 text-center text-slate-500">Updating analysis...</div>
            ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <FeatureImportance data={insights?.feature_importance} />

                    <div className="space-y-6">
                        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                                <Lightbulb className="w-5 h-5 text-amber-500" />
                                Key Drivers
                            </h3>
                            <p className="text-slate-600 leading-relaxed mb-4">
                                {insights?.seasonal_insight}
                            </p>
                            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
                                <div className="flex items-start gap-3">
                                    <Target className="w-5 h-5 text-blue-600 mt-0.5" />
                                    <div>
                                        <h4 className="font-medium text-slate-800">Accuracy Metrics</h4>
                                        <p className="text-sm text-slate-500 mt-1">
                                            Model MAPE (Mean Absolute Percentage Error) is currently <strong>{insights?.mape_score}%</strong>, well within tolerance.
                                        </p>
                                    </div>
                                </div>
                            </div>

                             {insights?.anomalies && insights.anomalies.length > 0 && (
                                <div className="mt-4 p-4 bg-amber-50 rounded-lg border border-amber-100">
                                    <div className="flex items-start gap-3">
                                        <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5" />
                                        <div>
                                            <h4 className="font-medium text-slate-800">Detected Anomalies</h4>
                                            <ul className="text-sm text-slate-600 mt-1 list-disc list-inside">
                                                {insights.anomalies.map((a, i) => (
                                                    <li key={i}><strong>{a.district}:</strong> {a.description}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="bg-gradient-to-br from-slate-900 to-slate-800 p-6 rounded-xl text-white shadow-md">
                            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                                <Zap className="w-5 h-5 text-yellow-400" />
                                Recommendation
                            </h3>
                            <p className="text-slate-300 text-sm leading-relaxed mb-4">
                                {insights?.recommendation}
                            </p>
                            <button 
                                onClick={() => setIsPlanOpen(true)}
                                className="w-full py-2 bg-white/10 hover:bg-white/20 text-white font-medium text-sm rounded-lg transition-colors border border-white/10"
                            >
                                Generate Distribution Plan
                            </button>
                        </div>
                    </div>
                </div>
            )}

            <DistributionPlanModal isOpen={isPlanOpen} onClose={() => setIsPlanOpen(false)} />
        </div>
    );
}

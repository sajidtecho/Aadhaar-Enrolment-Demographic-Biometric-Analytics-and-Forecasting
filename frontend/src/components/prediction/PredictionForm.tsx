import { useState, useEffect } from 'react';
import { ChevronDown, Loader2 } from 'lucide-react';
import { cn } from '../../utils/utils';
import { states as allStates, districts as allDistricts } from '../../utils/locations';

interface PredictionFormProps {
    onPredict: (data: any) => void;
    isLoading: boolean;
    initialType?: string;
}

export default function PredictionForm({ onPredict, isLoading, initialType = 'demand' }: PredictionFormProps) {
    const [formData, setFormData] = useState({
        state: '',
        district: '',
        type: initialType,
        horizon: '1',
        year: new Date().getFullYear(),
        month: new Date().getMonth() + 2, // Next month by default
        bio_age_5_17: 500,
        bio_age_17_: 1200,
        age_0_5: 150
    });
    
    // Update type when initialType changes
    useEffect(() => {
        setFormData(prev => ({ ...prev, type: initialType }));
    }, [initialType]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Map form type to backend expected values
        const payload = {
            ...formData,
            prediction_type: formData.type
        };
        onPredict(payload);
    };

    const states = ['All India', ...allStates];
    
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
            <h3 className="text-lg font-semibold text-slate-800 mb-4">Generate Forecast</h3>
            <form onSubmit={handleSubmit} className="space-y-4">

                {/* Model Type Selector - Only show if no initial type is set from URL */}
                {!initialType && (
                    <div className="grid grid-cols-3 gap-2 p-1 bg-slate-100 rounded-lg">
                        <button
                            type="button"
                            onClick={() => setFormData({...formData, type: 'demand'})}
                            className={cn(
                                "py-2 text-sm font-medium rounded-md transition-all",
                                formData.type === 'demand' 
                                    ? "bg-white text-blue-700 shadow-sm" 
                                    : "text-slate-500 hover:text-slate-700"
                            )}
                        >
                            Demographic Demand
                        </button>
                        <button
                            type="button"
                            onClick={() => setFormData({...formData, type: 'enrollment'})}
                            className={cn(
                                "py-2 text-sm font-medium rounded-md transition-all",
                                formData.type === 'enrollment' 
                                    ? "bg-white text-blue-700 shadow-sm" 
                                    : "text-slate-500 hover:text-slate-700"
                            )}
                        >
                            Operational Forecast
                        </button>
                        <button
                            type="button"
                            onClick={() => setFormData({...formData, type: 'biometric_load'})}
                            className={cn(
                                "py-2 text-sm font-medium rounded-md transition-all",
                                formData.type === 'biometric_load' 
                                    ? "bg-white text-blue-700 shadow-sm" 
                                    : "text-slate-500 hover:text-slate-700"
                            )}
                        >
                            Biometric Load
                        </button>
                    </div>
                )}
                
                {/* State Selection */}
                <div className="space-y-1.5">
                    <label className="text-sm font-medium text-slate-700">State</label>
                    <div className="relative">
                        <select
                            aria-label="Select State"
                            className="w-full pl-4 pr-10 py-2.5 bg-slate-50 border border-slate-200 rounded-lg appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm"
                            value={formData.state}
                            onChange={(e) => {
                                const newState = e.target.value;
                                setFormData({
                                    ...formData,
                                    state: newState,
                                    district: newState === 'All India' ? 'All Districts' : ''
                                });
                            }}
                            required
                        >
                            <option value="">Select State</option>
                            {states.map(s => <option key={s} value={s}>{s}</option>)}
                        </select>
                        <ChevronDown className="absolute right-3 top-3 w-4 h-4 text-slate-500 pointer-events-none" />
                    </div>
                </div>

                {/* District Selection */}
                <div className="space-y-1.5">
                    <label className="text-sm font-medium text-slate-700">District</label>
                    <div className="relative">
                        <select
                            aria-label="Select District"
                            className="w-full pl-4 pr-10 py-2.5 bg-slate-50 border border-slate-200 rounded-lg appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm disabled:opacity-50"
                            value={formData.district}
                            onChange={(e) => setFormData({ ...formData, district: e.target.value })}
                            required
                            disabled={!formData.state}
                        >
                            <option value="">Select District</option>
                            {formData.state === 'All India' && <option value="All Districts">All Districts</option>}
                            {formData.state && formData.state !== 'All India' && allDistricts[formData.state]?.map((d: string) => (
                                <option key={d} value={d}>{d}</option>
                            ))}
                        </select>
                        <ChevronDown className="absolute right-3 top-3 w-4 h-4 text-slate-500 pointer-events-none" />
                    </div>
                </div>

                {/* Date Selection */}
                <div className="grid grid-cols-2 gap-4">
                     <div className="space-y-1.5">
                        <label className="text-sm font-medium text-slate-700">Target Year</label>
                        <input 
                            type="number"
                            className="w-full pl-4 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={formData.year}
                            onChange={(e) => setFormData({...formData, year: parseInt(e.target.value)})}
                        />
                     </div>
                     <div className="space-y-1.5">
                        <label className="text-sm font-medium text-slate-700">Target Month</label>
                        <input 
                            type="number" min="1" max="12"
                            className="w-full pl-4 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={formData.month}
                            onChange={(e) => setFormData({...formData, month: parseInt(e.target.value)})}
                        />
                     </div>
                </div>



                <button
                    type="submit"
                    disabled={isLoading || !formData.state || !formData.district}
                    className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isLoading ? (
                        <>
                            <Loader2 className="w-4 h-4 animate-spin" />
                            <span>Processing...</span>
                        </>
                    ) : (
                        <span>Generate Prediction</span>
                    )}
                </button>
            </form>
        </div>
    );
}

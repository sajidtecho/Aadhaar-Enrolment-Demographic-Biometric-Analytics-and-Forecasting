import { useState } from 'react';
import { Server, Database, Activity, Terminal, AlertCircle, CheckCircle } from 'lucide-react';
import { verifyModelConnection } from '../services/api';
import { cn } from '../utils/utils';
import { states as allStates, districts as allDistricts } from '../utils/locations';

export default function ModelVerification() {
    const [formData, setFormData] = useState({ state: '', district: '', horizon: '1' });
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState<any>(null);
    const [logs, setLogs] = useState<any[]>([]);

    const states = allStates;
    const districts = allDistricts;

    const addLog = (type: 'req' | 'res' | 'err', content: any) => {
        setLogs(prev => [{
            timestamp: new Date().toLocaleTimeString(),
            type,
            content
        }, ...prev]);
    };

    const handleTest = async () => {
        setIsLoading(true);
        setResponse(null);
        
        // Calculate target date based on horizon
        const now = new Date();
        const targetDate = new Date(now.getFullYear(), now.getMonth() + parseInt(formData.horizon), 1);

        const payload = { 
            state: formData.state,
            district: formData.district,
            year: targetDate.getFullYear(),
            month: targetDate.getMonth() + 1,
            // Add dummy biometric values to satisfy schema
            bio_age_5_17: 1500, 
            bio_age_17_: 5000,
            timestamp: new Date().toISOString() 
        };

        addLog('req', { endpoint: '/api/predict', payload });

        const result = await verifyModelConnection(payload);

        if (result.success) {
            setResponse(result.data);
            addLog('res', { status: result.status, data: result.data });
        } else {
            setResponse({ error: result.error, details: result.details });
            addLog('err', { status: result.status, error: result.error });
        }

        setIsLoading(false);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
                        <Server className="w-6 h-6 text-blue-600" />
                        ML Model Integration Test Panel
                    </h1>
                    <p className="text-slate-500">Verify live connection to backend prediction engine</p>
                </div>
                <div className="flex items-center gap-2 px-3 py-1 bg-slate-100 rounded-full text-xs font-mono text-slate-600">
                    <Database className="w-3 h-3" />
                    Backend: http://localhost:8002
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                {/* Control Panel */}
                <div className="space-y-6">
                    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="text-sm font-semibold text-slate-800 mb-4 uppercase tracking-wider">Input Parameters</h3>
                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-1.5">
                                    <label className="text-xs font-medium text-slate-600">State</label>
                                    <select
                                        aria-label="Select State"
                                        className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm"
                                        value={formData.state}
                                        onChange={e => setFormData({ ...formData, state: e.target.value, district: '' })}
                                    >
                                        <option value="">Select State</option>
                                        {states.map(s => <option key={s} value={s}>{s}</option>)}
                                    </select>
                                </div>
                                <div className="space-y-1.5">
                                    <label className="text-xs font-medium text-slate-600">District</label>
                                    <select
                                        aria-label="Select District"
                                        className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm disabled:opacity-50"
                                        value={formData.district}
                                        onChange={e => setFormData({ ...formData, district: e.target.value })}
                                        disabled={!formData.state}
                                    >
                                        <option value="">Select District</option>
                                        {formData.state && (districts as any)[formData.state]?.map((d: string) => (
                                            <option key={d} value={d}>{d}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div className="space-y-1.5">
                                <label className="text-xs font-medium text-slate-600">Prediction Horizon</label>
                                <select
                                    aria-label="Select Horizon"
                                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm"
                                    value={formData.horizon}
                                    onChange={e => setFormData({ ...formData, horizon: e.target.value })}
                                >
                                    <option value="1">Next Month</option>
                                    <option value="3">Next 3 Months</option>
                                </select>
                            </div>

                            <button
                                onClick={handleTest}
                                disabled={isLoading || !formData.state || !formData.district}
                                className={cn(
                                    "w-full py-3 rounded-lg font-medium flex items-center justify-center gap-2 transition-all",
                                    isLoading ? "bg-slate-100 text-slate-400" : "bg-blue-600 text-white hover:bg-blue-700 shadow-md"
                                )}
                            >
                                {isLoading ? <Activity className="w-4 h-4 animate-spin" /> : <Server className="w-4 h-4" />}
                                {isLoading ? "Testing Connection..." : "Test Model Connection"}
                            </button>
                        </div>
                    </div>

                    {/* System Logs */}
                    <div className="bg-slate-900 rounded-xl border border-slate-800 shadow-sm overflow-hidden flex flex-col h-[300px]">
                        <div className="p-3 border-b border-slate-800 bg-slate-950 flex items-center justify-between">
                            <div className="flex items-center gap-2 text-slate-400">
                                <Terminal className="w-4 h-4" />
                                <span className="text-xs font-mono">System Logs</span>
                            </div>
                            <span className="flex h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
                        </div>
                        <div className="flex-1 p-4 font-mono text-xs overflow-y-auto space-y-3">
                            {logs.length === 0 && <span className="text-slate-600">Waiting for requests...</span>}
                            {logs.map((log, i) => (
                                <div key={i} className="flex gap-3">
                                    <span className="text-slate-500 whitespace-nowrap">[{log.timestamp}]</span>
                                    <div className={cn(
                                        "break-all",
                                        log.type === 'req' ? "text-blue-400" :
                                            log.type === 'res' ? "text-green-400" : "text-red-400"
                                    )}>
                                        <span className="font-bold uppercase mr-2">{log.type}:</span>
                                        {JSON.stringify(log.content)}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Results Panel */}
                <div className="space-y-6">
                    {response ? (
                        <div className="space-y-4">
                            {/* Success/Error Banner */}
                            <div className={cn(
                                "p-4 rounded-xl border flex items-center gap-3",
                                response.error
                                    ? "bg-red-50 border-red-200 text-red-700"
                                    : "bg-green-50 border-green-200 text-green-700"
                            )}>
                                {response.error ? <AlertCircle className="w-5 h-5" /> : <CheckCircle className="w-5 h-5" />}
                                <div>
                                    <h4 className="font-semibold">{response.error ? "Connection Failed" : "Verification Successful"}</h4>
                                    <p className="text-xs opacity-90">
                                        {response.error ? "API did not return a valid response." : "Data received from inference engine."}
                                    </p>
                                </div>
                            </div>

                            {!response.error && (
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                                        <h5 className="text-xs text-slate-500 uppercase tracking-wider mb-1">Predicted Value</h5>
                                        <p className="text-2xl font-bold text-slate-800">
                                            {response.prediction?.toLocaleString() || 'N/A'}
                                        </p>
                                    </div>
                                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                                        <h5 className="text-xs text-slate-500 uppercase tracking-wider mb-1">Risk Level</h5>
                                        <span className={cn(
                                            "px-2 py-1 rounded-full text-xs font-semibold",
                                            response.operationalMetrics?.peakPressureRatio > 1.2 ? "bg-red-100 text-red-700" : "bg-blue-100 text-blue-700"
                                        )}>
                                            {response.operationalMetrics?.peakPressureRatio > 1.2 ? "Critical Risk" : "Normal"}
                                        </span>
                                    </div>
                                </div>
                            )}

                            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                                <div className="p-3 border-b border-slate-100 bg-slate-50">
                                    <h3 className="text-xs font-semibold text-slate-700">Raw JSON Response</h3>
                                </div>
                                <div className="p-4 bg-slate-50 overflow-x-auto">
                                    <pre className="text-xs font-mono text-slate-600">
                                        {JSON.stringify(response, null, 2)}
                                    </pre>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="h-full bg-slate-50 border-2 border-dashed border-slate-200 rounded-xl flex flex-col items-center justify-center text-slate-400">
                            <Activity className="w-12 h-12 mb-4 opacity-20" />
                            <p className="font-medium">Ready to Test</p>
                            <p className="text-sm opacity-70">Initiate a request to see live results</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

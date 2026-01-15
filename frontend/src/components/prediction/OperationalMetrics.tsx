import { Activity, Gauge, TrendingUp } from 'lucide-react';

interface OperationalMetricsProps {
    metrics: {
        avgMonthlyLoad: number;
        peakPressureRatio: number;
        persistenceScore: number;
    };
}

export default function OperationalMetrics({ metrics }: OperationalMetricsProps) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden mt-6">
            <div className="p-4 border-b border-slate-100 bg-slate-50">
                <h3 className="text-sm font-semibold text-slate-800 flex items-center gap-2">
                    <Activity className="w-4 h-4 text-blue-600" />
                    Operational Stress & Capacity Analysis
                </h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-100">

                {/* Metric 1: Biometric Load */}
                <div className="p-6">
                    <div className="flex items-start justify-between mb-2">
                        <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Avg. Monthly Load</p>
                        <TrendingUp className="w-4 h-4 text-slate-400" />
                    </div>
                    <div className="flex items-baseline gap-2">
                        <h4 className="text-2xl font-bold text-slate-900">{metrics.avgMonthlyLoad.toLocaleString()}</h4>
                        <span className="text-xs text-slate-500">requests</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-2">Baseline capacity requirement per month.</p>
                </div>

                {/* Metric 2: Peak Pressure Ratio */}
                <div className="p-6">
                    <div className="flex items-start justify-between mb-2">
                        <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Peak Pressure Ratio</p>
                        <Gauge className="w-4 h-4 text-slate-400" />
                    </div>
                    <div className="flex items-baseline gap-2">
                        <h4 className={`text-2xl font-bold ${metrics.peakPressureRatio > 1.1 ? 'text-amber-600' : 'text-slate-900'}`}>
                            {metrics.peakPressureRatio}x
                        </h4>
                        <span className="text-xs text-slate-500">vs Normal</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-2">
                        {metrics.peakPressureRatio > 1.2
                            ? "High surge alert. Infrastructure strain likely."
                            : "Within safe operational limits."}
                    </p>
                </div>

                {/* Metric 3: Persistence Score */}
                <div className="p-6">
                    <div className="flex items-start justify-between mb-2">
                        <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Demand Persistence</p>
                        <Activity className="w-4 h-4 text-slate-400" />
                    </div>
                    <div className="flex items-center gap-2">
                        <h4 className="text-2xl font-bold text-slate-900">{metrics.persistenceScore}</h4>
                        <div className="flex-1 h-2 bg-slate-100 rounded-full ml-2 max-w-[80px]">
                            <div
                                className={`h-full rounded-full ${metrics.persistenceScore > 0.7 ? 'bg-red-500' : 'bg-blue-500'}`}
                                style={{ width: `${metrics.persistenceScore * 100}%` }}
                            ></div>
                        </div>
                    </div>
                    <p className="text-xs text-slate-400 mt-2">Probability of sustained high demand.</p>
                </div>

            </div>
        </div>
    );
}

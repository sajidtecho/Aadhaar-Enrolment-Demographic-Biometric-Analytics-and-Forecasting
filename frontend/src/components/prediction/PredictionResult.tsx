import { TrendingUp, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import OperationalMetrics from './OperationalMetrics';

interface PredictionResultProps {
    data: {
        prediction: number;
        confidence: number;
        trend: number;
        history: any[];
        operationalMetrics: {
            avgMonthlyLoad: number;
            peakPressureRatio: number;
            persistenceScore: number;
        };
    } | null;
}

export default function PredictionResult({ data }: PredictionResultProps) {
    if (!data) {
        return (
            <div className="h-full bg-slate-50 border border-dashed border-slate-300 rounded-xl flex flex-col items-center justify-center text-slate-400 p-8">
                <TrendingUp className="w-12 h-12 mb-3 opacity-20" />
                <p className="text-sm font-medium">Select parameters and generate a prediction to see results here.</p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white p-6 rounded-xl border border-blue-100 shadow-sm relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-full translate-x-10 -translate-y-10 opacity-50"></div>
                    <p className="text-sm font-medium text-slate-500 relative z-10">Predicted Volume</p>
                    <div className="flex items-baseline gap-2 mt-2 relative z-10">
                        <h2 className="text-4xl font-bold text-slate-900">{data.prediction.toLocaleString()}</h2>
                        <span className="text-sm font-medium text-green-600 bg-green-50 px-2 py-0.5 rounded-full">
                            +{data.trend}% vs last month
                        </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-2 relative z-10">
                        Model Confidence: <span className="text-slate-700 font-medium">{data.confidence}%</span>
                    </p>
                </div>

                <div className="md:col-span-2">
                    <OperationalMetrics metrics={data.operationalMetrics} />
                </div>

                <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <div className="flex items-start gap-4">
                        <div className={`p-2 rounded-lg ${data.trend > 10 ? 'bg-amber-50 text-amber-600' : 'bg-green-50 text-green-600'}`}>
                            {data.trend > 10 ? <AlertCircle className="w-6 h-6" /> : <CheckCircle2 className="w-6 h-6" />}
                        </div>
                        <div>
                            <h4 className="font-semibold text-slate-800">Operational Insight</h4>
                            <p className="text-sm text-slate-600 mt-1 leading-relaxed">
                                {data.trend > 10
                                    ? "High demand expected. Recommend increasing staff allocation by 15% and verifying kit functionality."
                                    : "Demand is stable. Standard operational capacity is sufficient. No immediate intervention required."}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <h4 className="text-sm font-semibold text-slate-800 mb-4">6-Month Trend Projection</h4>
                <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={data.history}>
                            <defs>
                                <linearGradient id="colorPred" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2} />
                                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} />
                            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} />
                            <Tooltip
                                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                            />
                            <Area type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorPred)" />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

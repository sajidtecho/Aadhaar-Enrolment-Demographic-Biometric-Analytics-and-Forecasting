import type { DistrictRisk } from '../../services/api';
import { cn } from '../../utils/utils';
import { AlertTriangle, AlertCircle, TrendingUp, Activity } from 'lucide-react';

const getStatusColor = (status: string) => {
    switch (status) {
        case 'Critical':
            return 'bg-red-50 text-red-700 border border-red-200';
        case 'High':
            return 'bg-orange-50 text-orange-700 border border-orange-200';
        case 'Medium':
            return 'bg-amber-50 text-amber-700 border border-amber-200';
        default:
            return 'bg-slate-50 text-slate-600 border border-slate-200';
    }
};

const getAnomalyType = (status: string, riskScore: number) => {
    if (status === 'Critical' || riskScore >= 85) return 'Sudden Demand Spike';
    if (status === 'High' || riskScore >= 70) return 'High Volume Pattern';
    if (status === 'Medium' || riskScore >= 50) return 'Moderate Activity';
    return 'Normal Pattern';
};

const getIcon = (status: string) => {
    switch (status) {
        case 'Critical':
            return <AlertTriangle className="w-4 h-4 text-red-500" />;
        case 'High':
            return <TrendingUp className="w-4 h-4 text-orange-500" />;
        case 'Medium':
            return <Activity className="w-4 h-4 text-amber-500" />;
        default:
            return <AlertCircle className="w-4 h-4 text-slate-400" />;
    }
};

export default function AnomalyTable({ districts }: { districts: DistrictRisk[] }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 text-slate-500 font-medium">
                        <tr>
                            <th className="px-6 py-4">District</th>
                            <th className="px-6 py-4">State</th>
                            <th className="px-6 py-4">Anomaly Type</th>
                            <th className="px-6 py-4 text-center">Risk Score</th>
                            <th className="px-6 py-4 text-center">Severity</th>
                            <th className="px-6 py-4 text-right">Predicted Load</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {districts.map((d) => (
                            <tr key={d.id} className="hover:bg-slate-50 transition-colors">
                                <td className="px-6 py-4 font-medium text-slate-900">{d.district}</td>
                                <td className="px-6 py-4 text-slate-600">{d.state}</td>
                                <td className="px-6 py-4 text-slate-600">
                                    <div className="flex items-center gap-2">
                                        {getIcon(d.status)}
                                        {getAnomalyType(d.status, d.riskScore)}
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="font-semibold text-slate-700">{d.riskScore}</span>
                                        <span className="text-xs text-slate-400">/100</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <span className={cn(
                                        "px-2.5 py-1 rounded-full text-xs font-medium",
                                        getStatusColor(d.status)
                                    )}>
                                        {d.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-right font-medium text-slate-700">
                                    {d.prediction.toLocaleString()}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                
                {districts.length === 0 && (
                    <div className="text-center py-12 text-slate-500">
                        <AlertCircle className="w-12 h-12 mx-auto mb-3 text-slate-300" />
                        <p className="font-medium">No anomalies found</p>
                        <p className="text-sm mt-1">Try adjusting the filters</p>
                    </div>
                )}
            </div>
        </div>
    );
}

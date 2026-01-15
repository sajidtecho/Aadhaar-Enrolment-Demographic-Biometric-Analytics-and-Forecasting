import type { DistrictRisk } from '../../services/mockData';
import { cn } from '../../utils/utils';
import { AlertTriangle, AlertCircle } from 'lucide-react';

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
                            <th className="px-6 py-4 text-center">Severity</th>
                            <th className="px-6 py-4 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {districts.map((d) => (
                            <tr key={d.id} className="hover:bg-slate-50 transition-colors">
                                <td className="px-6 py-4 font-medium text-slate-900">{d.district}</td>
                                <td className="px-6 py-4 text-slate-600">{d.state}</td>
                                <td className="px-6 py-4 text-slate-600">
                                    <div className="flex items-center gap-2">
                                        {d.riskScore > 90 ? <AlertTriangle className="w-4 h-4 text-red-500" /> : <AlertCircle className="w-4 h-4 text-amber-500" />}
                                        {d.riskScore > 90 ? 'Sudden Demand Spike' : 'Irregular Update Pattern'}
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <span className={cn(
                                        "px-2.5 py-1 rounded-full text-xs font-medium",
                                        d.riskScore > 90
                                            ? "bg-red-50 text-red-700 border border-red-200"
                                            : "bg-amber-50 text-amber-700 border border-amber-200"
                                    )}>
                                        {d.riskScore > 90 ? 'Critical' : 'Moderate'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <button className="text-blue-600 font-medium hover:text-blue-800 text-xs">
                                        View Details
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

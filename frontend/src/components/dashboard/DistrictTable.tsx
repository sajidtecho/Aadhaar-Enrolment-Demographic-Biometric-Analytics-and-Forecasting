import type { DistrictRisk } from '../../services/mockData';
import { cn } from '../../utils/utils';

export default function DistrictTable({ districts }: { districts: DistrictRisk[] }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-slate-100">
                <h3 className="text-lg font-semibold text-slate-800">High-Pressure Districts</h3>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 text-slate-500 font-medium">
                        <tr>
                            <th className="px-6 py-4">District</th>
                            <th className="px-6 py-4">State</th>
                            <th className="px-6 py-4 text-right">Pressure Score</th>
                            <th className="px-6 py-4 text-right">Predicted Load</th>
                            <th className="px-6 py-4">Status</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {districts.map((d) => (
                            <tr key={d.id} className="hover:bg-slate-50 transition-colors">
                                <td className="px-6 py-4 font-medium text-slate-900">{d.district}</td>
                                <td className="px-6 py-4 text-slate-600">{d.state}</td>
                                <td className="px-6 py-4 text-right">
                                    <div className="flex items-center justify-end gap-2">
                                        <span className="font-semibold">{d.riskScore}</span>
                                        <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                                            <div
                                                className={cn("h-full rounded-full", d.riskScore > 90 ? "bg-red-500" : "bg-amber-500")}
                                                style={{ width: `${d.riskScore}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-right text-slate-600">{d.prediction.toLocaleString()}</td>
                                <td className="px-6 py-4">
                                    <span className={cn(
                                        "px-2.5 py-1 rounded-full text-xs font-medium border",
                                        d.status === 'Critical' ? "bg-red-50 text-red-700 border-red-200" :
                                            d.status === 'High' ? "bg-orange-50 text-orange-700 border-orange-200" :
                                                "bg-blue-50 text-blue-700 border-blue-200"
                                    )}>
                                        {d.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

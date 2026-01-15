import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';
import { cn } from '../../utils/utils';
import type { Metric } from '../../services/mockData';

export default function KPICard({ metric }: { metric: Metric }) {
    const isPositive = metric.trend === 'up';
    const isNeutral = metric.trend === 'neutral';

    return (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <p className="text-sm font-medium text-slate-500 mb-1">{metric.label}</p>
            <div className="flex items-end justify-between">
                <h3 className="text-2xl font-bold text-slate-800">{metric.value}</h3>
                <div className={cn(
                    "flex items-center text-xs font-medium px-2 py-1 rounded-full",
                    isPositive ? "text-green-700 bg-green-50" :
                        isNeutral ? "text-slate-600 bg-slate-100" : "text-red-700 bg-red-50"
                )}>
                    {isPositive ? <ArrowUpRight className="w-3 h-3 mr-1" /> :
                        isNeutral ? <Minus className="w-3 h-3 mr-1" /> :
                            <ArrowDownRight className="w-3 h-3 mr-1" />}
                    {Math.abs(metric.change)}%
                </div>
            </div>
        </div>
    );
}

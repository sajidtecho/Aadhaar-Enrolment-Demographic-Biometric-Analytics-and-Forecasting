import { Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, ComposedChart } from 'recharts';
import type { TrendData } from '../../services/mockData';

export default function TrendChart({ data }: { data: TrendData[] }) {
    return (
        <div className="w-full">
            <ResponsiveContainer width="100%" height={300}>
                <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                        <linearGradient id="colorConfidence" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#8884d8" stopOpacity={0.1} />
                            <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: '#64748b' }} dy={10} />
                    <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b' }} />
                    <Tooltip
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    />
                    <Area
                        type="monotone"
                        dataKey="confidenceUpper"
                        stroke="none"
                        fill="url(#colorConfidence)"
                    />
                    <Area
                        type="monotone"
                        dataKey="confidenceLower"
                        stroke="none"
                        fill="#fff"
                    />
                    <Line
                        type="monotone"
                        dataKey="actual"
                        stroke="#2563eb"
                        strokeWidth={3}
                        dot={{ r: 4, fill: "#2563eb", strokeWidth: 2, stroke: "#fff" }}
                        activeDot={{ r: 6 }}
                        name="Actual Demand"
                    />
                    <Line
                        type="monotone"
                        dataKey="predicted"
                        stroke="#6366f1"
                        strokeWidth={3}
                        strokeDasharray="5 5"
                        dot={{ r: 4, fill: "#6366f1", strokeWidth: 2, stroke: "#fff" }}
                        name="Predicted Demand"
                    />
                </ComposedChart>
            </ResponsiveContainer>
        </div>
    );
}

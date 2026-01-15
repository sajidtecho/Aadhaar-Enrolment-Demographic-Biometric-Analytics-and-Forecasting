import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface FeatureData {
    name: string;
    value: number;
    color: string;
}

interface FeatureImportanceProps {
    data?: FeatureData[];
}

const defaultData = [
    { name: 'Loading...', value: 0, color: '#e2e8f0' }
];

export default function FeatureImportance({ data = defaultData }: FeatureImportanceProps) {
    if (!data || data.length === 0) data = defaultData;
    
    return (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-800 mb-6">Model Feature Importance</h3>
            <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart layout="vertical" data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                        <XAxis type="number" hide />
                        <YAxis
                            dataKey="name"
                            type="category"
                            width={120}
                            tick={{ fontSize: 12, fill: '#64748b' }}
                            axisLine={false}
                            tickLine={false}
                        />
                        <Tooltip
                            cursor={{ fill: 'transparent' }}
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={32}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

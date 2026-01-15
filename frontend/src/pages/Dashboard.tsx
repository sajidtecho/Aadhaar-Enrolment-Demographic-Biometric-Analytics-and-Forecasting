import { useEffect, useState } from 'react';
import KPICard from '../components/dashboard/KPICard';
import TrendChart from '../components/dashboard/TrendChart';
import DistrictTable from '../components/dashboard/DistrictTable';
import { getDashboardData } from '../services/api';
import type { DashboardResponse } from '../services/api';
import { Filter, Loader2, AlertTriangle } from 'lucide-react';

export default function Dashboard() {
    const [data, setData] = useState<DashboardResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await getDashboardData();
                setData(response);
                setError(null);
            } catch (err) {
                console.error("Failed to fetch dashboard data:", err);
                setError("Failed to load dashboard data. Please ensure backend is running.");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex h-96 items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
                <span className="ml-2 text-slate-600">Loading dashboard...</span>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="flex h-96 items-center justify-center flex-col">
                <AlertTriangle className="h-10 w-10 text-red-500 mb-2" />
                <p className="text-slate-800 font-medium">Error Loading Data</p>
                <p className="text-slate-500 text-sm mt-1">{error || "No data available."}</p>
                <button
                    onClick={() => window.location.reload()}
                    className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700"
                >
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Page Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Dashboard Overview</h1>
                    <p className="text-slate-500">Real-time predictive insights for UIDAI operations</p>
                </div>
                <div className="flex items-center gap-2">
                    <button className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50">
                        <Filter className="w-4 h-4" />
                        Filter View
                    </button>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 shadow-sm">
                        Export Report
                    </button>
                </div>
            </div>

            {/* KPI Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {data.kpi.map((metric, index) => (
                    <KPICard key={index} metric={metric} />
                ))}
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                    <TrendChart data={data.trend} />
                </div>
                <div className="lg:col-span-1">
                    <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl p-6 text-white h-full">
                        <h3 className="text-lg font-semibold mb-4">Urgent Actions</h3>
                        <ul className="space-y-4">
                            <li className="flex items-start gap-3 bg-white/10 p-3 rounded-lg backdrop-blur-sm">
                                <div className="w-2 h-2 rounded-full bg-red-400 mt-2"></div>
                                <div>
                                    <p className="font-medium text-sm">High Load in Pune</p>
                                    <p className="text-xs text-blue-100 opacity-80 mt-1">Deploy 4 additional kits to Haveli center immediately.</p>
                                </div>
                            </li>
                            <li className="flex items-start gap-3 bg-white/10 p-3 rounded-lg backdrop-blur-sm">
                                <div className="w-2 h-2 rounded-full bg-amber-400 mt-2"></div>
                                <div>
                                    <p className="font-medium text-sm">Anomaly in Bihar</p>
                                    <p className="text-xs text-blue-100 opacity-80 mt-1">Unusual spike in demographic updates detected.</p>
                                </div>
                            </li>
                        </ul>
                        <button className="w-full mt-6 py-2 bg-white text-blue-700 font-medium text-sm rounded-lg hover:bg-blue-50 transition-colors">
                            View All Alerts
                        </button>
                    </div>
                </div>
            </div>

            {/* District Table */}
            <DistrictTable districts={data.districts} />
        </div>
    );
}

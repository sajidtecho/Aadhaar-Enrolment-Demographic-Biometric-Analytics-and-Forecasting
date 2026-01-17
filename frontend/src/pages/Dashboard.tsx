import { useEffect, useState } from 'react';
import KPICard from '../components/dashboard/KPICard';
import TrendChart from '../components/dashboard/TrendChart';
import DistrictTable from '../components/dashboard/DistrictTable';
import { getDashboardData, getEnrollmentTrends } from '../services/api';
import type { DashboardResponse, TrendData } from '../services/api';
import { Loader2, AlertTriangle, Download, FileText, FileSpreadsheet } from 'lucide-react';
import { exportDashboardSummary } from '../utils/exportUtils';

export default function Dashboard() {
    const [data, setData] = useState<DashboardResponse | null>(null);
    const [enrollmentTrends, setEnrollmentTrends] = useState<TrendData[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showExportMenu, setShowExportMenu] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [dashData, enrolData] = await Promise.all([
                    getDashboardData(),
                    getEnrollmentTrends()
                ]);
                setData(dashData);
                setEnrollmentTrends(enrolData);
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
                    <p className="text-slate-500">Real-time data from trained ML models</p>
                    <div className="flex gap-3 mt-2">
                        <span className="text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded border border-blue-200">
                            📊 Biometric: 1.86M records
                        </span>
                        <span className="text-xs px-2 py-1 bg-green-50 text-green-700 rounded border border-green-200">
                            👥 Enrollment: 983K records
                        </span>
                    </div>
                </div>
                <div className="relative">
                    <button
                        onClick={() => setShowExportMenu(!showExportMenu)}
                        className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50"
                    >
                        <Download className="w-4 h-4" />
                        Export Summary
                    </button>
                    {showExportMenu && (
                        <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 z-10">
                            <button
                                onClick={() => {
                                    exportDashboardSummary(data?.kpi || [], data?.districts || [], 'csv');
                                    setShowExportMenu(false);
                                }}
                                className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm text-slate-600 hover:bg-slate-50 rounded-t-lg"
                            >
                                <FileSpreadsheet className="w-4 h-4" />
                                Export as CSV
                            </button>
                            <button
                                onClick={() => {
                                    exportDashboardSummary(data?.kpi || [], data?.districts || [], 'pdf');
                                    setShowExportMenu(false);
                                }}
                                className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm text-slate-600 hover:bg-slate-50"
                            >
                                <FileText className="w-4 h-4" />
                                Export as PDF
                            </button>
                            <button
                                onClick={() => {
                                    exportDashboardSummary(data?.kpi || [], data?.districts || [], 'word');
                                    setShowExportMenu(false);
                                }}
                                className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm text-slate-600 hover:bg-slate-50 rounded-b-lg"
                            >
                                <FileText className="w-4 h-4" />
                                Export as Word
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {/* KPI Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {data.kpi.map((metric, index) => (
                    <KPICard key={index} metric={metric} />
                ))}
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <h3 className="text-lg font-semibold text-slate-800">📊 Biometric Updates Trend</h3>
                            <p className="text-xs text-slate-500 mt-1">6-month historical + 1-month forecast</p>
                        </div>
                        <div className="flex items-center gap-4 text-xs">
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-blue-600"></span>
                                <span className="text-slate-600">Actual</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-indigo-500 border-2 border-dashed"></span>
                                <span className="text-slate-600">Predicted</span>
                            </div>
                        </div>
                    </div>
                    <TrendChart data={data.trend} />
                </div>
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <h3 className="text-lg font-semibold text-slate-800">👥 Enrollment Trend</h3>
                            <p className="text-xs text-slate-500 mt-1">6-month historical + 1-month forecast</p>
                        </div>
                        <div className="flex items-center gap-4 text-xs">
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-blue-600"></span>
                                <span className="text-slate-600">Actual</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-indigo-500 border-2 border-dashed"></span>
                                <span className="text-slate-600">Predicted</span>
                            </div>
                        </div>
                    </div>
                    {enrollmentTrends && <TrendChart data={enrollmentTrends} />}
                </div>
            </div>

            {/* District Risk Table */}
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
                <div className="px-6 py-4 border-b border-slate-100">
                    <h3 className="text-lg font-semibold text-slate-800">High Priority Districts (Real Data)</h3>
                    <p className="text-xs text-slate-500 mt-1">Top 5 districts by actual biometric update volume</p>
                </div>
                <DistrictTable districts={data.districts} />
            </div>
        </div>
    );
}

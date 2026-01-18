import { useState, useEffect, useMemo } from 'react';
import AnomalyTable from '../components/anomaly/AnomalyTable';
import { getAnomalies } from '../services/api';
import type { DistrictRisk } from '../services/api';
import { Filter, Download, Loader2, AlertTriangle, RefreshCw, FileText, FileSpreadsheet } from 'lucide-react';
import { exportAnomalies } from '../utils/exportUtils';

export default function AnomalyDetection() {
    const [statusFilter, setStatusFilter] = useState('All');
    const [stateFilter, setStateFilter] = useState('All');
    const [districtFilter, setDistrictFilter] = useState('All');
    const [showExportMenu, setShowExportMenu] = useState(false);
    
    const [districts, setDistricts] = useState<DistrictRisk[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await getAnomalies();
                setDistricts(response);
                setError(null);
            } catch (err: any) {
                console.error("Failed to fetch anomaly data:", err);
                const msg = err.response?.data?.detail 
                    || err.message 
                    || "Failed to load anomaly data from server.";
                setError(`${msg} (Please ensure backend is running at http://localhost:8002)`);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Extract unique states for dropdown
    const states = useMemo(() => {
        const unique = new Set(districts.map(d => d.state));
        return Array.from(unique).sort();
    }, [districts]);

    // Extract districts based on selected state
    const availableDistricts = useMemo(() => {
        if (stateFilter === 'All') return [];
        return districts
            .filter(d => d.state === stateFilter)
            .map(d => d.district)
            .sort();
    }, [districts, stateFilter]);

    // Main Filter Logic
    const filteredData = districts.filter(d => {
        const matchesStatus = statusFilter === 'All' ? true : d.status === statusFilter;
        const matchesState = stateFilter === 'All' ? true : d.state === stateFilter;
        const matchesDistrict = districtFilter === 'All' ? true : d.district === districtFilter;
        return matchesStatus && matchesState && matchesDistrict;
    });

    // Calculate statistics
    const stats = useMemo(() => {
        const criticalCount = districts.filter(d => d.status === 'Critical').length;
        const highCount = districts.filter(d => d.status === 'High').length;
        const mediumCount = districts.filter(d => d.status === 'Medium').length;
        const lowCount = districts.filter(d => d.status === 'Low').length;
        return { criticalCount, highCount, mediumCount, lowCount };
    }, [districts]);

    if (loading) {
        return (
            <div className="flex h-96 items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
                <span className="ml-2 text-slate-600">Scanning for anomalies...</span>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex h-96 items-center justify-center flex-col">
                <AlertTriangle className="h-10 w-10 text-red-500 mb-2" />
                <p className="text-slate-800 font-medium">System Error</p>
                <p className="text-slate-500 text-sm mt-1">{error}</p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Anomaly Detection</h1>
                    <p className="text-slate-500">Identify irregularities in biometric demand patterns across districts</p>
                </div>
                <div className="flex items-center gap-2">
                     <button onClick={() => window.location.reload()} className="p-2 text-slate-500 hover:text-blue-600 transition-colors">
                        <RefreshCw className="w-5 h-5" />
                    </button>
                    <div className="relative">
                        <button 
                            onClick={() => setShowExportMenu(!showExportMenu)}
                            className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50"
                        >
                            <Download className="w-4 h-4" />
                            Export Data
                        </button>
                        {showExportMenu && (
                            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 z-10">
                                <button
                                    onClick={() => {
                                        exportAnomalies(filteredDistricts, 'csv');
                                        setShowExportMenu(false);
                                    }}
                                    className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm text-slate-600 hover:bg-slate-50"
                                >
                                    <FileSpreadsheet className="w-4 h-4" />
                                    Export as CSV
                                </button>
                                <button
                                    onClick={() => {
                                        exportAnomalies(filteredDistricts, 'pdf');
                                        setShowExportMenu(false);
                                    }}
                                    className="w-full flex items-center gap-2 px-4 py-2 text-left text-sm text-slate-600 hover:bg-slate-50"
                                >
                                    <FileText className="w-4 h-4" />
                                    Export as PDF
                                </button>
                                <button
                                    onClick={() => {
                                        exportAnomalies(filteredDistricts, 'word');
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
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-xl border border-red-200 shadow-sm">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-xs font-medium text-red-600 uppercase tracking-wide">Critical</p>
                            <p className="text-2xl font-bold text-slate-800 mt-1">{stats.criticalCount}</p>
                        </div>
                        <div className="w-12 h-12 bg-red-50 rounded-lg flex items-center justify-center">
                            <AlertTriangle className="w-6 h-6 text-red-600" />
                        </div>
                    </div>
                </div>
                
                <div className="bg-white p-4 rounded-xl border border-orange-200 shadow-sm">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-xs font-medium text-orange-600 uppercase tracking-wide">High</p>
                            <p className="text-2xl font-bold text-slate-800 mt-1">{stats.highCount}</p>
                        </div>
                        <div className="w-12 h-12 bg-orange-50 rounded-lg flex items-center justify-center">
                            <AlertTriangle className="w-6 h-6 text-orange-600" />
                        </div>
                    </div>
                </div>
                
                <div className="bg-white p-4 rounded-xl border border-amber-200 shadow-sm">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-xs font-medium text-amber-600 uppercase tracking-wide">Medium</p>
                            <p className="text-2xl font-bold text-slate-800 mt-1">{stats.mediumCount}</p>
                        </div>
                        <div className="w-12 h-12 bg-amber-50 rounded-lg flex items-center justify-center">
                            <AlertTriangle className="w-6 h-6 text-amber-600" />
                        </div>
                    </div>
                </div>
                
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-xs font-medium text-slate-600 uppercase tracking-wide">Low</p>
                            <p className="text-2xl font-bold text-slate-800 mt-1">{stats.lowCount}</p>
                        </div>
                        <div className="w-12 h-12 bg-slate-50 rounded-lg flex items-center justify-center">
                            <AlertTriangle className="w-6 h-6 text-slate-400" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Filters Section */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center gap-2 text-slate-800 font-medium mb-2">
                    <Filter className="w-4 h-4 text-slate-500" />
                    Filter Data
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Status Filter */}
                    <div>
                        <label className="block text-xs font-medium text-slate-500 mb-1">Risk Severity</label>
                        <select 
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                            className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-700"
                        >
                            <option value="All">All Levels</option>
                            <option value="Critical">Critical</option>
                            <option value="High">High</option>
                            <option value="Medium">Medium</option>
                            <option value="Low">Low</option>
                        </select>
                    </div>

                    {/* State Filter */}
                    <div>
                        <label className="block text-xs font-medium text-slate-500 mb-1">State</label>
                        <select 
                            value={stateFilter}
                            onChange={(e) => {
                                setStateFilter(e.target.value);
                                setDistrictFilter('All'); // Reset district when state changes
                            }}
                            className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-700"
                        >
                            <option value="All">All States</option>
                            {states.map(state => (
                                <option key={state} value={state}>{state}</option>
                            ))}
                        </select>
                    </div>

                    {/* District Filter (Conditional) */}
                    <div>
                        <label className="block text-xs font-medium text-slate-500 mb-1">District</label>
                        <select 
                            value={districtFilter}
                            onChange={(e) => setDistrictFilter(e.target.value)}
                            disabled={stateFilter === 'All'}
                            className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-700 disabled:bg-slate-50 disabled:text-slate-400"
                        >
                            <option value="All">All Districts</option>
                            {availableDistricts.map(dist => (
                                <option key={dist} value={dist}>{dist}</option>
                            ))}
                        </select>
                    </div>
                </div>
                
                <div className="pt-2 text-xs text-slate-500 flex justify-end">
                    Showing {filteredData.length} records
                </div>
            </div>

            <AnomalyTable districts={filteredData} />
        </div>
    );
}

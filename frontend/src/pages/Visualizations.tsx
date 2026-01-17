import { useState, useEffect } from 'react';
import { BarChart3, Loader2, AlertTriangle, Image as ImageIcon, TrendingUp, Activity } from 'lucide-react';
import axios from 'axios';

interface Visual {
    name: string;
    path: string;
    category: string;
    title: string;
}

interface VisualsData {
    heatmaps: Visual[];
    lifecycle: Visual[];
    trends: Visual[];
    anomalies: Visual[];
}

const API_BASE = 'http://localhost:8002';

export default function Visualizations() {
    const [visuals, setVisuals] = useState<VisualsData>({
        heatmaps: [],
        lifecycle: [],
        trends: [],
        anomalies: []
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<string>('heatmaps');
    const [selectedImage, setSelectedImage] = useState<Visual | null>(null);

    useEffect(() => {
        fetchVisuals();
    }, []);

    const fetchVisuals = async () => {
        try {
            const response = await axios.get(`${API_BASE}/api/visuals/list`);
            setVisuals(response.data);
            setError(null);
        } catch (err) {
            console.error("Failed to fetch visualizations:", err);
            setError("Failed to load visualizations. Ensure backend is running.");
        } finally {
            setLoading(false);
        }
    };

    const getCategoryIcon = (category: string) => {
        switch (category) {
            case 'heatmaps':
                return <BarChart3 className="w-5 h-5" />;
            case 'lifecycle':
                return <Activity className="w-5 h-5" />;
            case 'trends':
                return <TrendingUp className="w-5 h-5" />;
            default:
                return <ImageIcon className="w-5 h-5" />;
        }
    };

    const getCategoryColor = (category: string) => {
        switch (category) {
            case 'heatmaps':
                return 'bg-red-50 text-red-600 border-red-200';
            case 'lifecycle':
                return 'bg-green-50 text-green-600 border-green-200';
            case 'trends':
                return 'bg-blue-50 text-blue-600 border-blue-200';
            default:
                return 'bg-gray-50 text-gray-600 border-gray-200';
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
                    <p className="text-slate-600">Loading visualizations...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="max-w-2xl mx-auto mt-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                    <div className="flex items-center gap-3 mb-2">
                        <AlertTriangle className="w-6 h-6 text-red-600" />
                        <h3 className="text-lg font-semibold text-red-800">Error Loading Visualizations</h3>
                    </div>
                    <p className="text-red-700">{error}</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    const currentVisuals = visuals[selectedCategory as keyof VisualsData] || [];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Data Visualizations</h1>
                    <p className="text-slate-500">Comprehensive visual analytics from all datasets</p>
                    <div className="flex gap-2 mt-2">
                        <span className="text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded border border-blue-200">
                            📊 Biometric: 1.86M records
                        </span>
                        <span className="text-xs px-2 py-1 bg-green-50 text-green-700 rounded border border-green-200">
                            👥 Enrollment: 983K records
                        </span>
                        <span className="text-xs px-2 py-1 bg-purple-50 text-purple-700 rounded border border-purple-200">
                            📈 Demographic: 1.6M records
                        </span>
                    </div>
                </div>
            </div>

            {/* Category Tabs */}
            <div className="bg-white rounded-xl border border-slate-200 p-4">
                <div className="flex gap-2">
                    {Object.keys(visuals).map((category) => {
                        const count = visuals[category as keyof VisualsData].length;
                        if (count === 0) return null;
                        
                        return (
                            <button
                                key={category}
                                onClick={() => setSelectedCategory(category)}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                                    selectedCategory === category
                                        ? getCategoryColor(category) + ' border'
                                        : 'text-slate-600 hover:bg-slate-50'
                                }`}
                            >
                                {getCategoryIcon(category)}
                                <span className="capitalize">{category}</span>
                                <span className="text-xs bg-white px-2 py-0.5 rounded-full border">
                                    {count}
                                </span>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Visualizations Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {currentVisuals.map((visual) => (
                    <div
                        key={visual.name}
                        className="bg-white rounded-xl border border-slate-200 overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
                        onClick={() => setSelectedImage(visual)}
                    >
                        <div className="aspect-video bg-slate-100 relative overflow-hidden">
                            <img
                                src={`${API_BASE}/api/${visual.path}`}
                                alt={visual.title}
                                className="w-full h-full object-contain hover:scale-105 transition-transform"
                                onError={(e) => {
                                    (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>';
                                }}
                            />
                        </div>
                        <div className="p-4">
                            <h3 className="font-semibold text-slate-800 mb-1">{visual.title}</h3>
                            <p className="text-sm text-slate-500 capitalize">{visual.category}</p>
                        </div>
                    </div>
                ))}
            </div>

            {currentVisuals.length === 0 && (
                <div className="text-center py-12">
                    <ImageIcon className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-slate-800 mb-2">No Visualizations Available</h3>
                    <p className="text-slate-500">
                        Run <code className="px-2 py-1 bg-slate-100 rounded">python generate_visuals.py</code> to create visualizations.
                    </p>
                </div>
            )}

            {/* Image Modal */}
            {selectedImage && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4"
                    onClick={() => setSelectedImage(null)}
                >
                    <div className="relative max-w-7xl max-h-full" onClick={(e) => e.stopPropagation()}>
                        <button
                            onClick={() => setSelectedImage(null)}
                            className="absolute -top-12 right-0 text-white hover:text-gray-300 text-2xl font-bold"
                        >
                            ✕
                        </button>
                        <img
                            src={`${API_BASE}/api/${selectedImage.path}`}
                            alt={selectedImage.title}
                            className="max-w-full max-h-[90vh] object-contain rounded-lg"
                        />
                        <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-75 text-white p-4 rounded-b-lg">
                            <h3 className="font-semibold text-lg">{selectedImage.title}</h3>
                            <p className="text-sm text-gray-300 capitalize">{selectedImage.category}</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

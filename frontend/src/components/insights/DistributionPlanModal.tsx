import { X, ArrowRight, Truck, CheckCircle } from 'lucide-react';
import { delhiCenters } from '../../services/delhi_centers';

interface TransferItem {
    from: string;
    to: string;
    kits: number;
    distance: string;
    impact: string;
}

interface DistributionPlanModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function DistributionPlanModal({ isOpen, onClose }: DistributionPlanModalProps) {
    if (!isOpen) return null;

    // Generate dynamic transfers based on real Delhi centers
    const transfers: TransferItem[] = [
        { 
            from: delhiCenters[3].name, // MCD School Badarpur
            to: delhiCenters[5].name,   // Saket Court
            kits: 45, 
            distance: '8.2 km', 
            impact: 'Reduces wait time by 2 days' 
        },
        { 
            from: delhiCenters[13].name, // Tekhand Village
            to: delhiCenters[0].name,    // SDM Office Kalkaji
            kits: 30, 
            distance: '4.5 km', 
            impact: 'Addresses critical shortage' 
        },
        { 
            from: delhiCenters[18].name, // Shahbad Mohammadpur
            to: delhiCenters[24].name,   // Vasant Kunj
            kits: 25, 
            distance: '12 km', 
            impact: 'Preventive allocation' 
        },
        { 
            from: delhiCenters[7].name,  // Lal Kuan
            to: delhiCenters[1].name,    // DC Office Saket
            kits: 15, 
            distance: '6.5 km', 
            impact: 'Balances load spike' 
        },
    ];

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
                
                {/* Header */}
                <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50">
                    <div>
                        <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                            <Truck className="w-5 h-5 text-blue-600" />
                            Optimized Resource Distribution Plan (Delhi Region)
                        </h2>
                        <p className="text-sm text-slate-500 mt-1">Generated based on predictive demand variance for South & New Delhi</p>
                    </div>
                    <button 
                        onClick={onClose} 
                        className="p-2 hover:bg-slate-200 rounded-full transition-colors text-slate-500"
                        aria-label="Close"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 overflow-y-auto">
                    <div className="mb-6 p-4 bg-blue-50 border border-blue-100 rounded-xl">
                        <h4 className="font-semibold text-blue-900 text-sm mb-2">Strategy Summary</h4>
                        <p className="text-sm text-blue-700 leading-relaxed">
                            The system has identified <strong>3 critical high-demand zones</strong> in South Delhi that will exceed capacity. Recommend immediate redistribution of <strong>115 biometric kits</strong> from lower utilization centers like {delhiCenters[3].name}.
                        </p>
                    </div>

                    <h3 className="text-sm font-semibold text-slate-700 uppercase tracking-wider mb-4">Recommended Transfers</h3>
                    
                    <div className="space-y-3">
                        {transfers.map((item, index) => (
                            <div key={index} className="flex items-center justify-between p-4 bg-white border border-slate-200 rounded-xl hover:border-blue-300 transition-colors shadow-sm">
                                <div className="flex items-center gap-6">
                                    <div className="text-center w-32">
                                        <div className="text-xs text-slate-400 font-medium uppercase mb-1">Source</div>
                                        <div className="font-semibold text-slate-700 text-sm truncate" title={item.from}>{item.from}</div>
                                    </div>
                                    
                                    <div className="flex flex-col items-center">
                                        <div className="text-xs font-mono text-slate-400 mb-1">{item.kits} Kits</div>
                                        <ArrowRight className="w-5 h-5 text-blue-500" />
                                        <div className="text-[10px] text-slate-400 mt-1">{item.distance}</div>
                                    </div>

                                    <div className="text-center w-32">
                                        <div className="text-xs text-slate-400 font-medium uppercase mb-1">Destination</div>
                                        <div className="font-semibold text-slate-700 text-sm truncate" title={item.to}>{item.to}</div>
                                    </div>
                                </div>
                                
                                <div className="hidden sm:block pl-6 border-l border-slate-100 w-48">
                                    <div className="flex items-start gap-2">
                                        <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5 shrink-0" />
                                        <span className="text-xs text-slate-600 font-medium">{item.impact}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
                    <button onClick={onClose} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded-lg transition-colors text-sm">
                        Dismiss
                    </button>
                    <button className="px-4 py-2 bg-blue-600 text-white font-medium hover:bg-blue-700 rounded-lg shadow-sm transition-colors text-sm flex items-center gap-2">
                        <Truck className="w-4 h-4" />
                        Initiate Transfers
                    </button>
                </div>
            </div>
        </div>
    );
}

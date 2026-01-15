export default function Header() {
    return (
        <header className="bg-white border-b border-slate-200 h-16 flex items-center px-8 fixed top-0 right-0 left-64 z-10">
            <div>
                <h2 className="text-lg font-semibold text-slate-800">Aadhaar Service Demand Prediction System</h2>
                <p className="text-xs text-slate-500">Data-driven insights for proactive UIDAI planning</p>
            </div>

            <div className="ml-auto flex items-center gap-4">
                <div className="px-3 py-1 bg-green-50 text-green-700 text-xs font-medium rounded-full border border-green-200">
                    System Operational
                </div>
                <div className="w-8 h-8 bg-slate-100 rounded-full flex items-center justify-center text-slate-600 text-sm font-medium">
                    SA
                </div>
            </div>
        </header>
    );
}

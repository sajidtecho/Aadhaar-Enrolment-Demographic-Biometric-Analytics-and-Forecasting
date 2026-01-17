import { LayoutDashboard, Fingerprint, Users, UserPlus, AlertTriangle, BarChart3, HelpCircle, ShieldCheck, Image } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { cn } from '../../utils/utils';

const navItems = [
    { name: 'Dashboard Overview', icon: LayoutDashboard, path: '/' },
    { name: 'Biometric Prediction', icon: Fingerprint, path: '/predict/biometric' },
    { name: 'Demographic Prediction', icon: Users, path: '/predict/demographic' },
    { name: 'Enrolment Prediction', icon: UserPlus, path: '/predict/enrolment' },
    { name: 'Anomaly Detection', icon: AlertTriangle, path: '/anomalies' },
    { name: 'Model Insights', icon: BarChart3, path: '/insights' },
    { name: 'Visualizations', icon: Image, path: '/visualizations' },
    { name: 'Verify Integration', icon: ShieldCheck, path: '/verify' },
    { name: 'About / Methodology', icon: HelpCircle, path: '/about' },
];

export default function Sidebar() {
    return (
        <div className="w-64 bg-white h-screen border-r border-slate-200 flex flex-col fixed left-0 top-0 z-10">
            <div className="p-6 border-b border-slate-100">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
                        A
                    </div>
                    <h1 className="text-xl font-bold text-slate-800">Aadhaar Analytics</h1>
                </div>
            </div>

            <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            cn(
                                "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
                                isActive
                                    ? "bg-blue-50 text-blue-700"
                                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                            )
                        }
                    >
                        <item.icon className="w-5 h-5" />
                        {item.name}
                    </NavLink>
                ))}
            </nav>

            <div className="p-4 border-t border-slate-100">
                <p className="text-xs text-slate-400 text-center">
                    © 2026 UIDAI Analytics<br />v1.0.0 (Policy-Grade)
                </p>
            </div>
        </div>
    );
}

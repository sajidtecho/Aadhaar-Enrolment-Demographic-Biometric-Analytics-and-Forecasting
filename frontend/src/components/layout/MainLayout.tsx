import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function MainLayout() {
    return (
        <div className="min-h-screen bg-slate-50">
            <Sidebar />
            <Header />
            <main className="pl-64 pt-16 min-h-screen">
                <div className="max-w-7xl mx-auto p-8">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}

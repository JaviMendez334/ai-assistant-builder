import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { Outlet } from "react-router-dom";

export default function DashboardLayout() {
  return (
    <div className="flex min-h-screen bg-[#030712] text-slate-100 relative selection:bg-blue-500/30 selection:text-white">
      {/* Luces ambientales de fondo */}
      <div className="fixed top-0 left-72 right-0 h-96 bg-gradient-to-b from-blue-600/5 via-indigo-500/5 to-transparent blur-3xl pointer-events-none -z-10" />
      <div className="fixed -bottom-40 right-10 w-96 h-96 bg-blue-600/5 rounded-full blur-3xl pointer-events-none -z-10" />

      {/* Barra Lateral Fija/Sticky */}
      <Sidebar />

      {/* Contenedor Principal */}
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />

        <main className="flex-1 p-6 md:p-10 max-w-7xl w-full mx-auto animate-fadeIn">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
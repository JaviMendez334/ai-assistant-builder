import { LogOut, User, Bell, Sparkles, Circle } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("token");
    navigate("/login");
  }

  return (
    <header className="h-16 sticky top-0 z-40 bg-slate-950/75 backdrop-blur-xl border-b border-slate-800/80 flex items-center justify-between px-6 md:px-10 transition-colors">
      {/* TÍTULO / INDICADOR DE ESTADO */}
      <div className="flex items-center gap-4">
        <h2 className="text-sm md:text-base font-semibold text-white tracking-tight flex items-center gap-2">
          Workspace Principal
        </h2>
        <span className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <Circle size={6} className="fill-emerald-400 animate-pulse" />
          API Online
        </span>
      </div>

      {/* ACCIONES Y PERFIL */}
      <div className="flex items-center gap-3">
        {/* Notificaciones / Feedback sutil */}
        <button
          title="Notificaciones"
          className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-900 rounded-xl transition-colors"
        >
          <Bell size={18} />
        </button>

        <div className="h-4 w-px bg-slate-800 mx-1" />

        {/* Perfil & Logout */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2.5 pl-2">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center font-bold text-xs shadow-md shadow-blue-600/20 border border-white/10">
              <User size={15} />
            </div>
            <div className="hidden md:block text-left">
              <p className="text-xs font-semibold text-slate-200 leading-tight">Admin</p>
              <p className="text-[10px] text-slate-400">Workspace Owner</p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            title="Cerrar sesión"
            className="flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-red-400 hover:bg-red-500/10 border border-transparent hover:border-red-500/20 px-3 py-1.5 rounded-xl transition-all duration-200 ml-2"
          >
            <LogOut size={15} />
            <span className="hidden sm:inline">Salir</span>
          </button>
        </div>
      </div>
    </header>
  );
}

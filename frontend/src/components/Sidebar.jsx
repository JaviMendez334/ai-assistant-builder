import {
  LayoutDashboard,
  Bot,
  FileText,
  MessageSquare,
  Settings,
  Sparkles,
  ChevronRight
} from "lucide-react";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  const links = [
    {
      name: "Dashboard",
      path: "/",
      icon: <LayoutDashboard size={19} />
    },
    {
      name: "Asistentes IA",
      path: "/assistants",
      icon: <Bot size={19} />
    },
    {
      name: "Documentos",
      path: "/documents",
      icon: <FileText size={19} />
    },
    {
      name: "Conversaciones",
      path: "/conversations",
      icon: <MessageSquare size={19} />
    },
    {
      name: "Configuración",
      path: "/settings",
      icon: <Settings size={19} />
    }
  ];

  return (
    <aside className="w-72 min-h-screen bg-slate-950/80 backdrop-blur-xl border-r border-slate-800/80 p-5 flex flex-col justify-between shrink-0 select-none">
      <div>
        {/* LOGO BRANDING */}
        <div className="flex items-center gap-3 px-3 py-4 mb-6 border-b border-slate-800/50">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/25 ring-1 ring-white/20">
            <Sparkles size={20} className="animate-pulse" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight leading-tight flex items-center gap-1.5">
              AI Assistant
              <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">PRO</span>
            </h1>
            <p className="text-xs text-slate-400 font-medium tracking-wide">
              Enterprise Builder
            </p>
          </div>
        </div>

        {/* MENU */}
        <nav className="space-y-1.5">
          <p className="px-3 text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
            Plataforma
          </p>
          {links.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                `group flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? "bg-blue-600 text-white shadow-lg shadow-blue-600/25 shadow-inner ring-1 ring-white/10"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/80"
                }`
              }
            >
              <div className="flex items-center gap-3">
                <span className="transition-transform duration-200 group-hover:scale-110">
                  {link.icon}
                </span>
                <span>{link.name}</span>
              </div>
              <ChevronRight size={14} className="opacity-0 group-hover:opacity-100 transition-opacity text-slate-400" />
            </NavLink>
          ))}
        </nav>
      </div>

      {/* FOOTER WIDGET */}
      <div className="pt-4 border-t border-slate-800/60">
        <div className="bg-gradient-to-b from-slate-900/90 to-slate-950 border border-slate-800/80 rounded-2xl p-4 shadow-sm relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-24 h-24 bg-blue-500/10 rounded-full blur-xl pointer-events-none" />
          
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-200">Plan Enterprise</span>
            <span className="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded-full font-medium">Activo</span>
          </div>

          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mb-2">
            <div className="bg-blue-500 h-full rounded-full w-2/3" />
          </div>

          <p className="text-[11px] text-slate-400 flex justify-between">
            <span>Capacidad RAG</span>
            <span className="text-slate-300 font-medium">Ilimitado</span>
          </p>
        </div>
      </div>
    </aside>
  );
}

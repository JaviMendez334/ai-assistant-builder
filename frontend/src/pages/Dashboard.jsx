import {
  Plus,
  Bot,
  FileText,
  MessageCircle,
  Activity,
  ArrowUpRight,
  Sparkles,
  Database,
  ArrowRight,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getProjects, getAssistants, getDocuments } from "../services/api";

function Dashboard() {
  const navigate = useNavigate();

  const [stats, setStats] = useState({
    assistantsCount: 0,
    documentsCount: 0,
    projectsCount: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardMetrics() {
      try {
        const projects = await getProjects();
        const totalProjects = projects.length;

        let totalAssistants = 0;
        let totalDocs = 0;

        if (totalProjects > 0) {
          const firstProjectId = projects[0].id;
          const [assistants, docs] = await Promise.all([
            getAssistants(firstProjectId).catch(() => []),
            getDocuments(firstProjectId).catch(() => []),
          ]);
          totalAssistants = assistants.length;
          totalDocs = docs.length;
        }

        setStats({
          projectsCount: totalProjects,
          assistantsCount: totalAssistants,
          documentsCount: totalDocs,
        });
      } catch (err) {
        console.error("Error cargando métricas:", err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardMetrics();
  }, []);

  return (
    <div className="space-y-10">
      {/* HEADER DE BIENVENIDA */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20 mb-3">
            <Sparkles size={13} className="text-blue-400" />
            Centro de Control & IA Generativa
          </div>
          <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight">
            Panel General
          </h1>
          <p className="text-slate-400 mt-1 text-sm md:text-base">
            Monitorea tus agentes RAG, bases de conocimiento y llamadas a herramientas.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate("/assistants")}
            className="bg-blue-600 hover:bg-blue-500 text-white font-medium px-5 py-2.5 rounded-xl flex items-center gap-2 text-sm shadow-lg shadow-blue-600/20 transition-all hover:scale-[1.02]"
          >
            <Plus size={18} />
            Nuevo Asistente
          </button>
        </div>
      </div>

      {/* METRICAS PRINCIPALES */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          icon={<Bot size={22} />}
          title="Asistentes Activos"
          value={loading ? "..." : stats.assistantsCount}
          subtitle="Agentes configurados"
          accent="blue"
        />
        <StatCard
          icon={<FileText size={22} />}
          title="Documentos RAG"
          value={loading ? "..." : stats.documentsCount}
          subtitle="PDFs indexados"
          accent="indigo"
        />
        <StatCard
          icon={<Database size={22} />}
          title="Espacios de Trabajo"
          value={loading ? "..." : stats.projectsCount}
          subtitle="Proyectos creados"
          accent="sky"
        />
        <StatCard
          icon={<Activity size={22} />}
          title="Motor de Inferencia"
          value="Groq / LLaMA"
          subtitle="Baja latencia"
          accent="emerald"
        />
      </div>

      {/* BANNER DE ACCION RÁPIDA (HERO CARD) */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-blue-700 via-indigo-700 to-slate-900 p-8 md:p-10 shadow-2xl border border-white/10">
        <div className="absolute -top-24 -right-24 w-80 h-80 bg-blue-400/20 rounded-full blur-3xl pointer-events-none" />
        
        <div className="max-w-2xl relative z-10">
          <span className="text-xs uppercase font-bold tracking-widest text-blue-200">
            Comienza ahora
          </span>
          <h2 className="text-2xl md:text-3xl font-bold text-white mt-2 leading-tight">
            Amplía el conocimiento de tus agentes con RAG
          </h2>
          <p className="text-blue-100 text-sm md:text-base mt-2 leading-relaxed">
            Sube manuales, catálogos o documentación técnica en PDF para que tu asistente responda preguntas precisas mediante recuperación semántica.
          </p>

          <div className="flex flex-wrap gap-4 mt-6">
            <button
              onClick={() => navigate("/documents")}
              className="bg-white text-slate-950 hover:bg-blue-50 font-semibold px-6 py-3 rounded-xl flex items-center gap-2 text-sm transition-all shadow-lg shadow-black/20"
            >
              <FileText size={17} />
              Gestionar Documentos
            </button>
            <button
              onClick={() => navigate("/assistants")}
              className="bg-slate-900/60 hover:bg-slate-900/80 text-white font-medium px-6 py-3 rounded-xl flex items-center gap-2 text-sm border border-white/20 backdrop-blur-md transition-all"
            >
              Ver Asistentes
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, title, value, subtitle, accent }) {
  const accentStyles = {
    blue: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    indigo: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
    sky: "bg-sky-500/10 text-sky-400 border-sky-500/20",
    emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 hover:border-slate-700/80 transition-all duration-200 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className={`p-2.5 rounded-xl border ${accentStyles[accent] || accentStyles.blue}`}>
            {icon}
          </div>
          <span className="text-[11px] text-slate-400 font-medium flex items-center gap-0.5">
            Métrica <ArrowUpRight size={13} />
          </span>
        </div>

        <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider">
          {title}
        </p>
        <h3 className="text-2xl md:text-3xl font-bold text-white mt-1 tracking-tight">
          {value}
        </h3>
      </div>

      <p className="text-slate-400 text-xs mt-3 pt-3 border-t border-slate-800/60">
        {subtitle}
      </p>
    </div>
  );
}

export default Dashboard;

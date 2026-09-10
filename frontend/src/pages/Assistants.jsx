import {
  Plus,
  Bot,
  Trash2,
  Sparkles,
  Users,
  MessageSquare,
  X,
  ArrowRight,
  FolderKanban,
  Loader2,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getProjects,
  getAssistants,
  createAssistant,
  deleteAssistant,
} from "../services/api";

export default function Assistants() {
  const navigate = useNavigate();

  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [assistants, setAssistants] = useState([]);
  const [loading, setLoading] = useState(true);

  // Estados del modal
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState("");
  const [instructions, setInstructions] = useState("");
  const [model, setModel] = useState("llama-3.1-8b-instant");
  const [creating, setCreating] = useState(false);

  // 1. Cargar proyectos al montar
  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await getProjects();
        setProjects(data);
        if (data.length > 0) {
          setSelectedProjectId(String(data[0].id));
        }
      } catch (error) {
        console.error("Error al cargar proyectos:", error);
      } finally {
        setLoading(false);
      }
    }
    loadProjects();
  }, []);

  // 2. Cargar asistentes cuando cambia el proyecto seleccionado
  useEffect(() => {
    if (!selectedProjectId) {
      setAssistants([]);
      return;
    }
    loadAssistants(selectedProjectId);
  }, [selectedProjectId]);

  async function loadAssistants(projectId) {
    try {
      setLoading(true);
      const data = await getAssistants(projectId);
      setAssistants(data);
    } catch (error) {
      console.error("Error cargando asistentes:", error);
      setAssistants([]);
    } finally {
      setLoading(false);
    }
  }

  // 3. Crear nuevo asistente
  async function handleCreateAssistant(e) {
    e.preventDefault();
    if (!selectedProjectId) return;

    try {
      setCreating(true);
      await createAssistant(selectedProjectId, {
        nombre: name,
        instrucciones: instructions,
        modelo: model,
      });

      setName("");
      setInstructions("");
      setShowModal(false);
      await loadAssistants(selectedProjectId);
    } catch (error) {
      alert(error.message || "Error creando asistente");
    } finally {
      setCreating(false);
    }
  }

  // 4. Eliminar asistente
  async function handleDeleteAssistant(e, assistantId) {
    e.stopPropagation();
    if (!window.confirm("¿Seguro que deseas eliminar este asistente?")) return;

    try {
      await deleteAssistant(assistantId);
      setAssistants((prev) => prev.filter((a) => a.id !== assistantId));
    } catch (error) {
      alert(error.message || "Error al eliminar el asistente");
    }
  }

  return (
    <div className="space-y-8">
      {/* HEADER */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="bg-blue-600/20 p-3 rounded-xl text-blue-400">
              <Sparkles size={28} />
            </div>
            <h1 className="text-3xl font-bold text-white">Asistentes IA</h1>
          </div>
          <p className="text-slate-400 mt-2">
            Crea agentes inteligentes para automatizar procesos y consultar tu base de conocimiento.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          disabled={!selectedProjectId}
          className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white px-6 py-3 rounded-xl flex items-center gap-2 text-sm font-medium transition shadow-lg shadow-blue-600/20"
        >
          <Plus size={20} />
          Nuevo asistente
        </button>
      </div>

      {/* SELECTOR DE PROYECTO */}
      {projects.length > 0 && (
        <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 p-4 rounded-xl w-fit">
          <FolderKanban size={18} className="text-blue-400" />
          <span className="text-slate-300 text-sm font-medium">Proyecto activo:</span>
          <select
            value={selectedProjectId}
            onChange={(e) => setSelectedProjectId(e.target.value)}
            className="bg-slate-950 border border-slate-800 text-white text-sm rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-500"
          >
            {projects.map((p) => (
              <option key={p.id} value={p.id}>
                {p.nombre || p.name || `Proyecto #${p.id}`}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* METRICAS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          icon={<Bot size={24} />}
          title="Asistentes en proyecto"
          value={assistants.length}
        />
        <StatCard
          icon={<Users size={24} />}
          title="Proyectos creados"
          value={projects.length}
        />
        <StatCard
          icon={<MessageSquare size={24} />}
          title="Pipeline activo"
          value="RAG + Tools"
        />
      </div>

      {/* LISTADO DE ASISTENTES */}
      {loading ? (
        <div className="text-slate-400 text-sm flex items-center gap-2">
          <Loader2 size={16} className="animate-spin text-blue-400" />
          Cargando asistentes...
        </div>
      ) : assistants.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center">
          <Bot size={40} className="mx-auto text-slate-600 mb-3" />
          <h3 className="text-white font-medium">No hay asistentes en este proyecto</h3>
          <p className="text-slate-400 text-sm mt-1 mb-4">
            Crea tu primer agente para interactuar con tus documentos.
          </p>
          <button
            onClick={() => setShowModal(true)}
            className="text-blue-400 hover:text-blue-300 text-sm font-medium"
          >
            Crear asistente &rarr;
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {assistants.map((assistant) => (
            <div
              key={assistant.id}
              onClick={() => navigate(`/assistants/${assistant.id}`)}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-slate-700 transition cursor-pointer flex flex-col justify-between"
            >
              <div>
                <div className="flex justify-between items-start">
                  <div className="bg-blue-600/20 text-blue-400 p-4 rounded-xl">
                    <Bot size={28} />
                  </div>
                  <button
                    onClick={(e) => handleDeleteAssistant(e, assistant.id)}
                    title="Eliminar asistente"
                    className="text-slate-500 hover:text-red-400 transition-colors p-1"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>

                <h2 className="text-xl font-semibold text-white mt-5">
                  {assistant.nombre}
                </h2>

                <p className="text-slate-400 text-sm mt-2 line-clamp-3">
                  {assistant.instrucciones || "Sin instrucciones específicas."}
                </p>
              </div>

              <div className="flex justify-between items-center mt-6 pt-4 border-t border-slate-800/80">
                <span className="bg-blue-500/10 text-blue-400 text-xs px-2.5 py-1 rounded-full border border-blue-500/20 font-mono">
                  {assistant.modelo}
                </span>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/assistants/${assistant.id}`);
                  }}
                  className="flex items-center gap-1.5 text-blue-400 hover:text-blue-300 text-sm font-medium"
                >
                  Probar
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* MODAL CREAR ASISTENTE */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-lg shadow-2xl">
            <div className="flex justify-between items-center mb-5">
              <h2 className="text-xl font-bold text-white">Crear Nuevo Asistente</h2>
              <button
                onClick={() => setShowModal(false)}
                className="text-slate-400 hover:text-white"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleCreateAssistant} className="space-y-4">
              <div>
                <label className="block text-slate-300 text-xs font-medium mb-1.5">
                  Nombre del Asistente
                </label>
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Ej: Asistente de Ventas"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-slate-300 text-xs font-medium mb-1.5">
                  Modelo LLM
                </label>
                <select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 text-white text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:border-blue-500"
                >
                  <option value="llama-3.1-8b-instant">llama-3.1-8b-instant (Rápido)</option>
                  <option value="llama-3.3-70b-versatile">llama-3.3-70b-versatile (Preciso)</option>
                  <option value="mixtral-8x7b-32768">mixtral-8x7b-32768</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-300 text-xs font-medium mb-1.5">
                  Instrucciones del Sistema (System Prompt)
                </label>
                <textarea
                  value={instructions}
                  onChange={(e) => setInstructions(e.target.value)}
                  placeholder="Instrucciones sobre el rol, tono y reglas que debe seguir el modelo..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-white text-sm h-32 focus:outline-none focus:border-blue-500"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={creating}
                className="w-full bg-blue-600 hover:bg-blue-500 text-white py-3 rounded-xl font-medium text-sm transition mt-2 disabled:bg-slate-800"
              >
                {creating ? "Creando agente..." : "Crear asistente"}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ icon, title, value }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
      <div className="text-blue-400 mb-3">{icon}</div>
      <p className="text-slate-400 text-xs font-medium uppercase tracking-wider">{title}</p>
      <h3 className="text-2xl font-bold text-white mt-1">{value}</h3>
    </div>
  );
}

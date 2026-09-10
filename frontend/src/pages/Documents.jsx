import {
  Upload,
  FileText,
  Trash2,
  CheckCircle,
  Loader2,
  FolderKanban,
} from "lucide-react";
import { useEffect, useState, useRef } from "react";
import { useSearchParams } from "react-router-dom";
import {
  getProjects,
  getDocuments,
  uploadDocument,
  deleteDocument,
} from "../services/api";

export default function Documents() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialProjectId = searchParams.get("project") || "";

  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(initialProjectId);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const fileInputRef = useRef(null);

  // 1. Cargar la lista de proyectos disponibles
  useEffect(() => {
    async function fetchProjects() {
      try {
        const data = await getProjects();
        setProjects(data);
        if (data.length > 0 && !selectedProjectId) {
          setSelectedProjectId(String(data[0].id));
        }
      } catch (err) {
        setErrorMsg("No se pudieron cargar los proyectos.");
      } finally {
        setLoading(false);
      }
    }
    fetchProjects();
  }, []);

  // 2. Cargar documentos cuando cambia el proyecto seleccionado
  useEffect(() => {
    if (!selectedProjectId) return;

    setSearchParams({ project: selectedProjectId });
    loadDocuments(selectedProjectId);
  }, [selectedProjectId]);

  async function loadDocuments(projectId) {
    try {
      setLoading(true);
      setErrorMsg("");
      const data = await getDocuments(projectId);
      setDocuments(data);
    } catch (err) {
      setErrorMsg(err.message || "Error al cargar documentos.");
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  }

  // 3. Manejador para subir documento
  async function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file || !selectedProjectId) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      alert("Por favor selecciona un archivo PDF.");
      return;
    }

    setUploading(true);
    setErrorMsg("");

    try {
      await uploadDocument(selectedProjectId, file);
      await loadDocuments(selectedProjectId);
    } catch (err) {
      alert("Error al subir el archivo: " + err.message);
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  }

  // 4. Manejador para eliminar documento
  async function handleDeleteDocument(documentId) {
    if (!window.confirm("¿Seguro que deseas eliminar este documento y sus fragmentos RAG?")) {
      return;
    }

    try {
      await deleteDocument(documentId);
      setDocuments((prev) => prev.filter((doc) => doc.id !== documentId));
    } catch (err) {
      alert("Error al eliminar documento: " + err.message);
    }
  }

  return (
    <div className="space-y-8">
      {/* HEADER */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Base de Conocimiento</h1>
          <p className="text-slate-400 mt-1">
            Gestiona los documentos PDF utilizados por los asistentes RAG.
          </p>
        </div>

        {/* Input Oculto y Botón de Subida */}
        <div className="flex items-center gap-3">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".pdf"
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading || !selectedProjectId}
            className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white px-5 py-2.5 rounded-xl flex items-center gap-2 text-sm font-medium transition-colors shadow-lg shadow-blue-600/20"
          >
            {uploading ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Procesando Chunks...
              </>
            ) : (
              <>
                <Upload size={18} />
                Subir PDF
              </>
            )}
          </button>
        </div>
      </div>

      {/* SELECTOR DE PROYECTO */}
      {projects.length > 0 && (
        <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 p-4 rounded-xl w-fit">
          <FolderKanban size={18} className="text-blue-400" />
          <span className="text-slate-300 text-sm font-medium">Proyecto:</span>
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

      {errorMsg && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl text-sm">
          {errorMsg}
        </div>
      )}

      {/* LISTADO DE DOCUMENTOS */}
      {loading ? (
        <div className="text-slate-400 text-sm flex items-center gap-2">
          <Loader2 size={16} className="animate-spin text-blue-400" />
          Cargando documentos...
        </div>
      ) : documents.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center">
          <FileText size={40} className="mx-auto text-slate-600 mb-3" />
          <h3 className="text-white font-medium">No hay documentos en este proyecto</h3>
          <p className="text-slate-400 text-sm mt-1 mb-4">
            Sube un archivo PDF para habilitar el contexto RAG en tus asistentes.
          </p>
          <button
            onClick={() => fileInputRef.current?.click()}
            className="text-blue-400 hover:text-blue-300 text-sm font-medium"
          >
            Subir mi primer documento &rarr;
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition flex flex-col justify-between"
            >
              <div>
                <div className="flex justify-between items-start">
                  <div className="bg-blue-600/20 text-blue-400 p-3 rounded-xl">
                    <FileText size={24} />
                  </div>

                  <button
                    onClick={() => handleDeleteDocument(doc.id)}
                    title="Eliminar documento"
                    className="text-slate-500 hover:text-red-400 transition-colors p-1"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>

                <h2 className="text-base font-semibold text-white mt-4 break-all">
                  {doc.filename || doc.name}
                </h2>

                <p className="text-slate-500 text-xs mt-1">
                  ID: {doc.id} {doc.created_at ? `• ${new Date(doc.created_at).toLocaleDateString()}` : ""}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-center justify-between">
                <span className="flex items-center gap-1.5 bg-green-500/10 text-green-400 px-2.5 py-1 rounded-full text-xs font-medium border border-green-500/20">
                  <CheckCircle size={13} />
                  Indexado (RAG)
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

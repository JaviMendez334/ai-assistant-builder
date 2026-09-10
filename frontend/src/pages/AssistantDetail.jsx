import {
  Bot,
  ArrowLeft,
  MessageSquare,
  Send,
  FileText,
  User,
  Loader2,
} from "lucide-react";
import { useEffect, useState, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getAssistant, sendChatMessage } from "../services/api";

export default function AssistantDetail() {
  const { assistantId } = useParams();
  const navigate = useNavigate();

  const [assistant, setAssistant] = useState(null);
  const [loading, setLoading] = useState(true);

  // Estados del Chat
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  async function loadAssistant() {
    try {
      const data = await getAssistant(assistantId);
      setAssistant(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAssistant();
  }, [assistantId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSendMessage(e) {
    e.preventDefault();
    if (!inputMessage.trim() || sending) return;

    const userText = inputMessage;
    setInputMessage("");
    setMessages((prev) => [...prev, { role: "user", content: userText }]);
    setSending(true);

    try {
      const data = await sendChatMessage(assistantId, userText);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.respuesta },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Error: " + (error.message || "No se pudo obtener respuesta"),
        },
      ]);
    } finally {
      setSending(false);
    }
  }

  if (loading) {
    return <div className="text-slate-400 p-6">Cargando asistente...</div>;
  }

  if (!assistant) {
    return <div className="text-white p-6">Asistente no encontrado</div>;
  }

  return (
    <div className="space-y-6">
      <button
        onClick={() => navigate("/assistants")}
        className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors"
      >
        <ArrowLeft size={18} />
        Volver
      </button>

      {/* Encabezado del Asistente */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-5">
          <div className="bg-blue-600/20 text-blue-400 p-4 rounded-xl">
            <Bot size={36} />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">{assistant.nombre}</h1>
            <p className="text-slate-400 text-sm mt-1">
              Modelo: <span className="text-blue-400">{assistant.modelo}</span>
            </p>
          </div>
        </div>

        <button
          onClick={() => navigate(`/documents?project=${assistant.project_id}`)}
          className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-xl text-sm font-medium border border-slate-700 transition-colors self-start md:self-auto"
        >
          <FileText size={16} />
          Ver Documentos del Proyecto
        </button>
      </div>

      {/* Grid Principal: Playground de Chat + Información */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Ventana de Chat */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col h-[560px] overflow-hidden">
          <div className="p-4 border-b border-slate-800 flex items-center gap-2 text-white font-medium text-sm">
            <MessageSquare size={16} className="text-blue-400" />
            Playground de Prueba (RAG + Tools)
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-slate-500 text-sm">
                <Bot size={32} className="mb-2 opacity-50" />
                Haz una pregunta para probar el conocimiento del asistente.
              </div>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex gap-3 ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  {msg.role === "assistant" && (
                    <div className="w-8 h-8 rounded-lg bg-blue-600/20 text-blue-400 flex items-center justify-center shrink-0">
                      <Bot size={18} />
                    </div>
                  )}

                  <div
                    className={`max-w-[80%] rounded-xl p-3 text-sm leading-relaxed whitespace-pre-wrap ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-slate-800 text-slate-200 border border-slate-700"
                    }`}
                  >
                    {msg.content}
                  </div>

                  {msg.role === "user" && (
                    <div className="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 flex items-center justify-center shrink-0">
                      <User size={18} />
                    </div>
                  )}
                </div>
              ))
            )}
            {sending && (
              <div className="flex items-center gap-2 text-slate-400 text-sm italic">
                <Loader2 size={16} className="animate-spin text-blue-400" />
                El asistente está procesando y consultando herramientas...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Formulario de Entrada */}
          <form
            onSubmit={handleSendMessage}
            className="p-3 border-t border-slate-800 bg-slate-950/50 flex gap-2"
          >
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Escribe un mensaje..."
              disabled={sending}
              className="flex-1 bg-slate-900 border border-slate-800 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={sending || !inputMessage.trim()}
              className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white px-4 py-2.5 rounded-xl transition-colors shrink-0"
            >
              <Send size={16} />
            </button>
          </form>
        </div>

        {/* Panel Lateral: Instrucciones y Configuración */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 h-fit space-y-4">
          <h2 className="text-white font-semibold text-lg">System Prompt</h2>
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 text-slate-300 text-sm leading-relaxed max-h-[420px] overflow-y-auto whitespace-pre-wrap">
            {assistant.instrucciones || "Sin instrucciones específicas configuradas."}
          </div>
        </div>
      </div>
    </div>
  );
}

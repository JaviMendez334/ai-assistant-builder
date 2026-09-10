# AI Assistant Builder & RAG Platform

Plataforma Fullstack modular para la creación, gestión y orquestación de agentes inteligentes de IA orientados al ámbito empresarial, integrando recuperación de información contextual (**RAG**) y ejecución dinámica de funciones (**Function Calling / Tools**).

---

## Características Principales

* **Orquestación de Agentes con Tool Calling:** Flujo de razonamiento en 2 rondas con invocación automática de herramientas (`search_documents`) mediante modelos LLM (Groq / Gemini API).
* **Pipeline RAG Completo:** Extracción de texto desde archivos PDF, particionado semántico (*chunking*), almacenamiento de fragmentos y búsqueda contextual aislada por proyecto.
* **Persistencia y Memoria Conversacional:** Registro relacional de sesiones, mensajes por rol (*system, user, assistant, tool*) y reglas de inferencia para prevenir alucinaciones.
* **Autenticación y Seguridad:** API protegida con JWT (OAuth2 Password Flow) y aislamiento de recursos multi-tenant por usuario y proyecto.
* **Frontend Reactivo:** Interfaz moderna desarrollada en React + Vite con Tailwind CSS, incluyendo panel de métricas, explorador de documentos y playground de chat interactivo.

---

## Arquitectura del Sistema

```text
[ React + Vite Frontend ]
           │  (REST API + JWT)
           ▼
[ FastAPI Backend ] ──► [ SQLAlchemy + SQLite / PostgreSQL ]
     │         │
     │         ├──► [ Ingesta de PDFs / Chunking / Search ]
     │
     ▼ (Function Calling Loop)
[ Groq / Gemini LLM API ]

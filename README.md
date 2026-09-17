# AI Assistant Builder & Business Engine

Plataforma SaaS full-stack multi-tenant diseñada para la **creación, parametrización, gestión y orquestación masiva de asistentes virtuales inteligentes con IA** para múltiples empresas y proyectos comerciales. Permite a los usuarios diseñar agentes a la medida configurando su identidad comercial (*system prompts*, roles, temperatura), asignar dinámicamente capacidades operativas (*Tool Calling* determinista), cargar bases de conocimiento documental para respuestas fundamentadas (*RAG local con SentenceTransformers*) y desplegar la interacción mediante un panel administrativo en React o de forma omnicanal a través de WhatsApp Business con la Meta Cloud API.

---

## Problema

La implementación de inteligencia artificial en entornos empresariales y comercios se topa comúnmente con barreras operativas significativas:
* **Falta de contexto y especialización:** Los bots conversacionales generales carecen de conocimiento específico sobre el negocio, alucinando datos de inventario, precios o políticas internas.
* **Desconexión con bases de datos vivas:** Las soluciones tradicionales no permiten que el modelo de lenguaje interactúe de forma segura y directa con el sistema operativo para consultar stock, actualizar existencias o registrar transacciones.
* **Rigidez en la creación de agentes:** Configurar asistentes con diferentes propósitos (atención al cliente, soporte interno, preventa, gestión de cartera) suele requerir desarrollos independientes complejos desde cero.
* **Vulnerabilidades de aislamiento multi-empresa:** Administrar múltiples marcas o clientes en una misma infraestructura sin un control riguroso de seguridad expone los datos a cruces y fugas de información crítica.

---

## Solución

**AI Assistant Builder & Business Engine** funciona como un ecosistema modular de ingeniería backend y orquestación de IA:
* **Constructor y Ciclo de Vida de Asistentes:** Módulo completo para crear y configurar asistentes con identidades independientes, instrucciones de sistema y selección flexible de modelos LLM.
* **Vinculación Modular de Herramientas (*Tool Binding*):** Asignación granular de capacidades operativas específicas a cada asistente según su rol (búsqueda en catálogo, modificación de inventario, consultas RAG y sincronización con hojas de cálculo).
* **Gestión Jerárquica por Proyectos:** Organización centralizada de los asistentes, archivos y bases de conocimiento agrupados en proyectos vinculados a cada empresa inquilina (*tenant*).
* **Base de Conocimiento Documental (RAG Local):** Ingesta de archivos PDF procesados, fragmentados y vectorizados localmente mediante `SentenceTransformers` (`all-MiniLM-L6-v2`) con reordenamiento semántico (*reranker*), permitiendo a los asistentes consultar información almacenada en documentos empresariales y utilizarla como contexto relevante.
* **Infoperación Omnicanal (WhatsApp Business):** Despliegue de los asistentes hacia interfaces web administrativas (React SPA) o canales de mensajería instantánea mediante la Meta Cloud API para automatizar procesos y atender clientes directamente.

---

## Características Principales

### Constructor y Motor de Asistentes (Core)
* Gestor de identidad y prompts dedicados con niveles de temperatura y modelos configurables.
* Estructura jerárquica de proyectos para agrupar agentes y fuentes documentales por tenant.
* Asignación dinámica de herramientas operativas según el caso de uso del asistente (`assistant_tool`).
* Persistencia estructurada de sesiones y conversaciones en base de datos.

### Base de Conocimiento y Pipeline RAG
* Extracción y saneamiento de texto estructurado desde archivos PDF (`document_processor.py`).
* Segmentación vectorial configurable (chunking) persistida en bases de datos relacionales (`models/chunk.py`).
* Generación local de embeddings mediante `SentenceTransformers` (`all-MiniLM-L6-v2`) operando con caché local.
* Búsqueda semántica y reordenamiento contextual con servicio de reranker (`reranker_service.py`).

### Motor Operativo, Inventario y Multi-Tenancy
* Aislamiento relacional multi-tenant mediante validación estricta de `tenant_id` en cada consulta.
* Tool Calling determinista acoplado directamente a procedimientos en PostgreSQL (`backend/tools/executor.py`).
* Carga masiva y normalización de catálogos mediante hojas de cálculo Excel (`.xlsx`).
* Ajustes de inventario por lenguaje natural (operaciones de restar, sumar y fijar).
* Conector de webhook con Meta WhatsApp Cloud API para procesamiento de mensajes y adjuntos.
* Panel SPA administrativo en React + Vite para monitoreo y configuración integral.
* Versionado estructurado y evolutivo del esquema de base de datos mediante Alembic (14 migraciones).

---

## Arquitectura del Sistema

```mermaid
flowchart TD
    subgraph Canales ["Canales e Interfaces"]
        AdminUI["Panel Web React SPA"]
        ChatWhatsApp["Meta WhatsApp Cloud API"]
    end

    subgraph Backend ["Plataforma Central FastAPI"]
        RouterAPI["API Routers: /assistants, /projects, /documents, /chat, /whatsapp, /excel"]
        
        subgraph Engine ["Motor del Asistente"]
            AssistantMgr["Assistant & Project Service"]
            ToolBinder["Assistant Tool Service"]
            AIEngine["AI Engine & Tool Loop"]
            RAGService["RAG Service & Embeddings Locales"]
        end
        
        subgraph Tools ["Registro de Herramientas"]
            T_Stock["update_product_stock"]
            T_Prod["search_products"]
            T_Docs["search_documents RAG"]
            T_Sheets["sheets_tool"]
        end
    end

    subgraph DB ["Capa de Persistencia"]
        Postgres[(PostgreSQL DB)]
        LocalCache[SentenceTransformers Cache]
    end

    AdminUI <--> RouterAPI
    ChatWhatsApp <--> RouterAPI
    RouterAPI --> AssistantMgr
    AssistantMgr --> AIEngine
    ToolBinder --> AIEngine
    AIEngine --> T_Stock & T_Prod & T_Docs & T_Sheets
    AIEngine <--> RAGService
    T_Stock & T_Prod & T_Sheets <--> Postgres
    RAGService <--> Postgres
    RAGService <--> LocalCache
```

---

## Arquitectura de IA y RAG

* **Modelos y Proveedores:** Integración principal con Groq SDK (modelos LLaMA 3.x para baja latencia en invocación de herramientas) y compatibilidad estructurada con Google Gemini SDK.
* **Bucle de Ejecución de Herramientas (*Tool Calling*):**
  1. Captura del mensaje entrante e inyección del *system prompt* del asistente activo junto al contexto del `tenant_id` y `project_id`.
  2. Evaluación de intención del LLM emitiendo estructuras de llamada a función (`tool_calls`).
  3. Ejecución controlada y síncrona mediante `backend/tools/executor.py` contra PostgreSQL.
  4. Envío de resultados estructurados al modelo para la síntesis de una respuesta final coherente.
* **Pipeline RAG Local:**
  * **Modelo de Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`.
  * **Ingesta y Segmentación:** Lectura de PDFs mediante `document_processor.py` y partición en fragmentos (`chunking.py`).
  * **Recuperación Semántica:** Búsqueda sobre la tabla `chunks` y optimización de relevancia contextual a través de `reranker_service.py`.

---

## Sistema de Herramientas (Tool Registry)

Las herramientas se registran de forma desacoplada y se asignan a cada asistente según su función operativa:

| Herramienta | Operación | Parámetros Principales | Descripción | Estado |
|---|---|---|---|---|
| `search_documents` | RAG / Vectorial | `query: str` | Recupera contexto de fragmentos documentales asociados al proyecto del asistente. | Implementado |
| `search_products` | Lectura (`SELECT`) | `query: str` | Consulta referencias, marcas y precios en el catálogo de productos del tenant. | Implementado |
| `update_product_stock` | Mutación (`UPDATE`) | `producto: str`, `cantidad: int`, `operacion: str` | Descuenta unidades vendidas, añade reposiciones o ajusta el stock físico real. | Implementado |
| `sheets_tool` | Integración API | Parámetros de hoja | Conexión y sincronización de datos con Google Sheets mediante credenciales de servicio. | Implementado |

---

## Stack Tecnológico

### Backend
* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI, Uvicorn
* **Persistencia & ORM:** PostgreSQL, SQLAlchemy, Alembic
* **Validación y DTOs:** Pydantic
* **Procesamiento de Archivos:** Pandas, OpenPyXL, PyPDF2
* **NLP & IA:** PyTorch, Sentence-Transformers, Groq SDK, Google GenAI SDK
* **Cliente HTTP:** HTTPX

### Frontend
* **Entorno & Bundler:** Node.js, Vite
* **Librería UI:** React 18+
* **Estilos:** TailwindCSS / CSS modular
* **Consumo API:** Fetch / Axios (`src/services/api.js`)

---

## Estructura del Proyecto

```text
.
├── backend/
│   ├── alembic/                 # Migraciones versionadas de base de datos
│   │   ├── versions/            # 14 revisiones históricas de esquemas relacionales
│   │   └── env.py
│   ├── config/                  # Ajustes globales y credenciales
│   │   ├── google_credentials.json
│   │   └── settings.py
│   ├── database/                # Conexiones, sesión y utilidades de creación
│   │   ├── connection.py
│   │   ├── create_tables.py
│   │   ├── database.py
│   │   └── session.py
│   ├── models/                  # Entidades relacionales (SQLAlchemy)
│   │   ├── project.py           # Agrupación de proyectos por empresa
│   │   ├── assistant.py         # Configuración, prompts y modelos de asistentes
│   │   ├── assistant_tool.py    # Asignación de herramientas a asistentes
│   │   ├── document.py          # Metadatos de archivos subidos
│   │   ├── chunk.py             # Fragmentos de texto con vectores de embeddings
│   │   ├── conversation.py      # Sesiones de conversación
│   │   ├── product.py           # Catálogo de productos e inventario
│   │   ├── tenant.py            # Empresas e inquilinos registrados
│   │   └── user.py              # Usuarios y roles del sistema
│   ├── routers/                 # Endpoints organizados por dominio
│   │   ├── assistants.py        # CRUD y configuración de asistentes virtuales
│   │   ├── projects.py          # Administración de proyectos por empresa
│   │   ├── documents.py         # Carga y gestión documental para RAG
│   │   ├── chat.py              # Interfaz de chat directa vía REST
│   │   ├── conversations.py     # Consulta y persistencia de historial conversacional
│   │   ├── excel_upload.py      # Ingesta masiva de inventarios
│   │   ├── auth.py              # Registro, autenticación y emisión JWT
│   │   ├── home.py, profile.py
│   │   └── whatsapp.py          # Webhook receptor y despachador de Meta Cloud API
│   ├── schemas/                 # Validación de payloads y DTOs (Pydantic)
│   │   ├── assistant.py, auth.py, chat.py, chunk.py
│   │   ├── conversation.py, document.py, project.py, user.py
│   ├── services/                # Reglas de negocio y procesamiento de IA
│   │   ├── assistant_service.py # Ciclo de vida y gestión de asistentes
│   │   ├── assistant_tool_service.py # Vinculación dinámica de herramientas
│   │   ├── project_service.py   # Lógica operativa de proyectos
│   │   ├── ai_engine.py         # Motor de inferencia y loop de tool calling
│   │   ├── rag_service.py       # Orquestación de recuperación semántica
│   │   ├── embedding_service.py # Generación local de embeddings
│   │   ├── chunking.py          # Algoritmos de particionado documental
│   │   ├── chunk_service.py     # Persistencia y consulta de fragmentos
│   │   ├── document_processor.py# Extracción de contenido en PDFs
│   │   ├── document_service.py  # Metadatos documentales
│   │   ├── reranker_service.py  # Reordenamiento semántico de relevancia
│   │   ├── excel_service.py     # Procesamiento y normalización de hojas de cálculo
│   │   ├── excel_importer.py    # Inserción masiva de productos
│   │   ├── chat_service.py, conversation_service.py, memory_service.py
│   │   ├── llm_service.py, search_service.py, tool_service.py, user_service.py
│   │   └── admin_commands.py, admin_tools.py
│   ├── tools/                   # Registro y clases ejecutables por el LLM
│   │   ├── base.py              # Clase base para herramientas
│   │   ├── executor.py          # Despachador determinista de funciones
│   │   ├── registry.py, registry_class.py # Registro singleton de herramientas
│   │   ├── products_tool.py     # Consulta de catálogo e inventario
│   │   ├── update_stock_tool.py # Modificación de existencias
│   │   ├── search_documents_tool.py # Recuperación documental RAG
│   │   ├── sheets_tool.py       # Conexión externa con Google Sheets
│   │   └── builtins/search_documents.py
│   ├── utils/                   # Seguridad, dependencias de FastAPI y tokens JWT
│   │   ├── dependencies.py, jwt.py, security.py
│   ├── alembic.ini
│   ├── main.py                  # Entrypoint principal de la API FastAPI
│   └── requirements.txt
├── frontend/                    # Panel administrativo en React + Vite
│   ├── src/
│   │   ├── pages/               # Dashboard, Assistants, AssistantDetail, Documents, Importer, Login, Register, Settings
│   │   ├── components/          # ExcelUploader, Navbar, Sidebar, ProtectedRoute
│   │   ├── layouts/             # DashboardLayout, MainLayout
│   │   ├── services/api.js      # Cliente de consumo HTTP contra FastAPI
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── test_gemini.py               # Test de integración con Google Gemini
├── test_groq.py                 # Test de inferencia y tools con Groq
├── test_pdf.py                  # Test de lectura y segmentación de PDFs
├── test_rag.py                  # Test del motor RAG
└── test_search.py               # Test de búsqueda semántica local
```

---

## Instalación y Configuración

### 1. Clonación del Repositorio
```bash
git clone https://github.com/JaviMendez334/ai-assistant-builder.git
cd ai-assistant-builder
```

### 2. Configuración del Backend

**En Windows (PowerShell):**
```powershell
python -m venv .venv
.\\.venv\\Scripts\\activate
pip install -r backend/requirements.txt
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 3. Configuración del Frontend
```bash
cd frontend
npm install
cd ..
```

---

## Variables de Entorno

Configura un archivo `.env` en el directorio raíz basándote en la siguiente plantilla:

```ini
# Base de Datos PostgreSQL
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db

# Proveedores LLM
GROQ_API_KEY=gsk_tu_clave_de_groq
GEMINI_API_KEY=tu_clave_de_gemini

# WhatsApp Business (Meta Cloud API)
WHATSAPP_ACCESS_TOKEN=tu_token_de_meta
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_VERIFY_TOKEN=token_definido_para_el_webhook

# Seguridad y Autenticación
SECRET_KEY=clave_secreta_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## Ejecución Local

### 1. Migraciones de Base de Datos
```bash
alembic -c backend/alembic.ini upgrade head
```

### 2. Iniciar Backend (FastAPI)
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
* **Swagger UI / Documentación interactiva:** `http://localhost:8000/docs`
* **Webhook WhatsApp:** `http://localhost:8000/api/v1/whatsapp/webhook`

### 3. Iniciar Frontend (React + Vite)
En otra terminal:
```bash
cd frontend
npm run dev
```
Disponible en: `http://localhost:5173`

### 4. Conexión del Webhook con Meta (Túnel Ngrok)
```bash
ngrok http 8000
```
Registra la URL generada (`[https://xxxx.ngrok-free.app/api/v1/whatsapp/webhook](https://xxxx.ngrok-free.app/api/v1/whatsapp/webhook)`) en el panel de configuración de WhatsApp dentro de Meta Developers.

---

## Pruebas y Validación

El proyecto incluye scripts independientes en la raíz para validar integraciones de forma aislada:

```bash
# Validar inferencia y llamadas a función con Groq
python test_groq.py

# Validar conectividad con Google Gemini
python test_gemini.py

# Validar extracción y lectura de documentos PDF
python test_pdf.py

# Validar el pipeline RAG y búsqueda semántica local
python test_rag.py
python test_search.py
```

---

## Capturas de Pantalla

* `docs/images/dashboard.png` - Panel de control y métricas generales
* `docs/images/assistants_builder.png` - Creación, parametrización y asignación de herramientas al asistente
* `docs/images/excel_upload.png` - Módulo de carga masiva de catálogos
* `docs/images/whatsapp_demo.png` - Consultas operativas y ajuste de existencias por WhatsApp

---

## Roadmap

El objetivo del proyecto es proporcionar una base robusta para desarrollar asistentes de IA empresariales capaces de consultar información propia de cada negocio y automatizar procesos comerciales mediante herramientas especializadas.

- [x] Arquitectura SaaS multi-tenant con aislamiento relacional por `tenant_id`.
- [x] Constructor de asistentes virtuales con prompts, roles y modelos independientes.
- [x] Organización de asistentes y bases de conocimiento agrupados por proyectos.
- [x] Asignación dinámica y modular de herramientas por asistente (`assistant_tool`).
- [x] Motor RAG local sobre archivos PDF con SentenceTransformers y reranker.
- [x] Despliegue omnicanal vía WhatsApp Cloud API y panel administrativo web en React.
- [x] Ingesta automática y ajuste de inventarios vía Excel y lenguaje natural.
- [ ] Ejecución atómica unificada de transacciones comerciales y descuento de stock.
- [ ] Suite formal de tests automatizados con `pytest` y base de datos de prueba aislada.
- [ ] Integración de búsqueda vectorial nativa con extensión `pgvector` sobre PostgreSQL.

---

## Seguridad

* **Aislamiento Multi-Tenant Estricto:** Validación y filtrado obligatorio del `tenant_id` en cada consulta relacional para impedir fugas entre empresas.
* **Gestión Criptográfica de Credenciales:** Hashing seguro de contraseñas mediante `bcrypt` y validación de sesiones sin estado vía tokens JWT.
* **Saneamiento y Tipado de Datos:** Esquemas Pydantic aplicados rigurosamente en la entrada y salida de cada endpoint REST.
* **Protección de Variables Sensibles:** Aislamiento total de credenciales y claves de API fuera del historial de Git.

---

## Autor

**Javier Andrés Estupiñán Méndez**  
Desarrollador Backend Junior | Integración de IA & Automatización

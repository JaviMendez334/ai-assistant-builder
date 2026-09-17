AI Assistant Builder & Business EngineSistema multi-tenant full-stack para la creación, parametrización y orquestación operativa de asistentes virtuales con modelos de lenguaje (LLM). Integra un motor RAG (Retrieval-Augmented Generation) local, ejecución de herramientas deterministas (Tool Calling), sincronización de existencias desde hojas de cálculo y canales de mensajería mediante Meta WhatsApp Cloud API junto con una interfaz web administrativa en React.🎯 ProblemaLa operación comercial y de atención al cliente en pequeñas y medianas empresas suele enfrentarse a desconexiones críticas entre sus herramientas de comunicación y sus fuentes de datos:Catálogos en hojas de cálculo que quedan rápidamente desfasados, provocando ventas sin existencias reales.Pérdida de control en cuentas por cobrar al gestionar créditos y abonos de manera informal en chats de mensajería.Respuestas inconsistentes o alucinaciones sobre condiciones comerciales, manuales y políticas de negocio.Dificultad técnica para operar múltiples marcas o unidades de negocio en una sola infraestructura sin mezclar la información de cada una.💡 SoluciónAI Assistant Builder & Business Engine conecta la base de datos relacional y los documentos de cada empresa con interfaces de mensajería y web:Aislamiento Multi-Tenant Lógico: Las consultas y mutaciones se filtran de forma determinista mediante tenant_id, impidiendo fugas de datos entre distintos comercios.Procesamiento de Archivos Tabulares y Documentales: Ingesta de archivos .xlsx y .pdf para actualizar catálogos de productos y alimentar bases de conocimiento RAG.Tool Calling Estructurado: El modelo de lenguaje delega las consultas de precios, bajas de existencias y balances a funciones en Python que interactúan directamente con PostgreSQL.✨ Características✅ Aislamiento Multi-Tenant: Filtro estricto por tenant_id en modelos ORM para productos, transacciones, conversaciones y fragmentos documentales.✅ Orquestación con Tool Calling: Invocación síncrona de herramientas para consultar catálogos, alterar existencias y consultar estados de cuenta.✅ Ingesta Automatizada de Catálogos: Carga de inventarios mediante archivos Excel (.xlsx) enviados por WhatsApp o cargados desde la API/Frontend.✅ Ajustes de Inventario en Lenguaje Natural: Herramienta dedicada con soporte para operaciones de descuento (restar), reposición (sumar) o ajuste de stock absoluto (fijar).✅ Pipeline RAG Local: Embeddings locales sin dependencias de red recurrentes con SentenceTransformers (all-MiniLM-L6-v2), segmentación documental (chunking) y reordenamiento semántico (reranker_service).✅ Canal WhatsApp Empresarial: Webhook con Meta Cloud API para verificación del handshake (hub.challenge), recepción de eventos de texto/archivos y envío de respuestas con formato estructurado.✅ Panel de Administración Web: Interfaz SPA en React + Vite para gestión de asistentes, carga de documentos, visualización de conversaciones e importación de datos.✅ Control de Migraciones: Versionado formal de esquemas relacionales mediante Alembic.🚧 Transacción Unificada Venta-Descuento: Integración atómica entre el registro contable de cartera y el descuento físico de stock en una sola llamada.📋 Indexación Vectorial Integrada: Migración del almacenamiento de vectores hacia extensiones nativas como pgvector.🏗️ ArquitecturaFragmento de códigoflowchart TD
    subgraph Canales
        UserWA([Cliente / Operador en WhatsApp]) <--> MetaCloud[Meta WhatsApp Cloud API]
        AdminWeb([Administrador / Operador Web]) <--> WebSPA[Frontend React SPA]
    end

    subgraph API Gateway FastAPI
        MetaCloud <--> WebhookWA[/api/v1/whatsapp/webhook/]
        WebSPA <--> RouterAuth[/api/v1/auth/]
        WebSPA <--> RouterCore[/api/v1/projects, /assistants, /documents, /excel/]
    end

    subgraph Orquestación y Lógica
        WebhookWA --> SessionResolver[Tenant & Conversation Resolver]
        RouterCore --> SessionResolver
        SessionResolver --> AIEngine[AI Engine & Tool Loop]
        AIEngine <--> LLMProvider[Groq SDK / Gemini API]
        
        AIEngine --> ToolExec[Tool Executor & Registry]
        ToolExec --> ToolStock[update_product_stock]
        ToolExec --> ToolProd[search_products]
        ToolExec --> ToolDocs[search_documents RAG]
        ToolExec --> ToolSheets[sheets_tool]
        
        WebhookWA --> ExcelService[Excel Service / Importer]
    end

    subgraph Capa de Datos
        ToolStock <--> Postgres[(PostgreSQL)]
        ToolProd <--> Postgres
        ExcelService --> Postgres
        ToolDocs <--> Postgres
        ToolDocs <--> EmbeddingsCache[SentenceTransformers Local Cache]
    end
🤖 Arquitectura de IA y RAGModelos y Proveedores: Integración principal con Groq SDK (modelos LLaMA 3.x para baja latencia en invocación de herramientas) y soporte modular para Google Gemini SDK.Bucle de Ejecución de Herramientas:Captura del mensaje entrante e inyección del system prompt del asistente junto al contexto del tenant_id.Generación de la llamada a función (tool_calls) según los esquemas JSON definidos.Ejecución directa y controlada en base de datos vía backend/tools/executor.py.Ronda de síntesis final donde el modelo genera la respuesta con base en la salida de la base de datos.Pipeline RAG Local:Modelo de Embeddings: sentence-transformers/all-MiniLM-L6-v2.Procesamiento Documental: Ingesta de archivos (document_processor.py), división de texto en fragmentos (chunking.py), almacenamiento de fragmentos con sus vectores en PostgreSQL y reordenamiento semántico (reranker_service.py).🧰 Tools / Function CallingHerramientaOperaciónParámetrosDescripciónEstadosearch_productsLectura (SELECT)query: strBusca coincidencias en el catálogo de productos filtrado por tenant_id.✅ Implementadoupdate_product_stockMutación (UPDATE)producto: str, cantidad: int, operacion: str (restar, sumar, fijar)Modifica las existencias de un producto validando disponibilidad previa.✅ Implementadosearch_documentsBúsqueda Semánticaquery: strRecupera fragmentos de texto vectorizados asociados al proyecto del asistente.✅ Implementadosheets_toolIntegración ExternaVariables de hojaConsulta y sincronización contra Google Sheets mediante cuenta de servicio.✅ Implementado📦 Stack TecnológicoBackendLenguaje: Python 3.10+Framework Web: FastAPI, UvicornPersistencia & ORM: PostgreSQL, SQLAlchemy, AlembicValidación de Datos: PydanticProcesamiento de Archivos: Pandas, OpenPyXL, PyPDF2NLP & IA: PyTorch, Sentence-Transformers, Groq SDK, Google GenAI SDKCliente HTTP: HTTPXFrontendEntorno & Bundler: Node.js, ViteLibrería UI: React 18+Estilos: TailwindCSS / CSS modularConsumo API: Fetch / Axios (src/services/api.js)  📁 Estructura del ProyectoPlaintext.
├── backend/
│   ├── alembic/                 # Migraciones versionadas de base de datos
│   │   ├── versions/            # 14 revisiones históricas de esquemas
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
│   │   ├── assistant.py, assistant_tool.py, chunk.py, conversation.py
│   │   ├── document.py, product.py, project.py, tenant.py, user.py
│   ├── routers/                 # Endpoints organizados por dominio
│   │   ├── assistants.py, auth.py, chat.py, conversations.py, documents.py
│   │   ├── excel_upload.py, home.py, profile.py, projects.py, whatsapp.py
│   ├── schemas/                 # Validación de payloads y DTOs (Pydantic)
│   │   ├── assistant.py, auth.py, chat.py, chunk.py
│   │   ├── conversation.py, document.py, project.py, user.py
│   ├── services/                # Reglas de negocio y procesamiento de IA
│   │   ├── admin_commands.py, admin_tools.py, ai_engine.py, assistant_service.py
│   │   ├── assistant_tool_service.py, chat_service.py, chunk_service.py, chunking.py
│   │   ├── conversation_service.py, document_processor.py, document_service.py
│   │   ├── embedding_service.py, excel_importer.py, excel_service.py, llm_service.py
│   │   ├── memory_service.py, project_service.py, rag_service.py, reranker_service.py
│   │   ├── search_service.py, tool_service.py, user_service.py
│   ├── tools/                   # Registro y clases ejecutables por el LLM
│   │   ├── base.py, executor.py, products_tool.py, registry.py
│   │   ├── registry_class.py, search_documents_tool.py, sheets_tool.py, update_stock_tool.py
│   │   └── builtins/search_documents.py
│   ├── utils/                   # Seguridad, dependencias de FastAPI y tokens JWT
│   │   ├── dependencies.py, jwt.py, security.py
│   ├── alembic.ini
│   ├── main.py                  # Entrypoint principal de la API
│   └── requirements.txt
├── frontend/                    # Panel administrativo en React
│   ├── src/
│   │   ├── components/          # ExcelUploader, Navbar, ProtectedRoute, Sidebar
│   │   ├── layouts/             # DashboardLayout, MainLayout
│   │   ├── pages/               # Dashboard, Assistants, Documents, Importer, Login, etc.
│   │   ├── services/            # Cliente de integración HTTP
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── test_gemini.py               # Test de integración con Google Gemini
├── test_groq.py                 # Test de inferencia y tools con Groq
├── test_pdf.py                  # Test de lectura y segmentación de PDFs
├── test_rag.py                  # Test del flujo de recuperación RAG
└── test_search.py               # Test de búsqueda semántica vectorial local
⚙️ Instalación y Configuración1. Clonación del RepositorioBashgit clone https://github.com/tu-usuario/ai-assistant-builder.git
cd ai-assistant-builder
2. Configuración del BackendEn Windows (PowerShell):PowerShellpython -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
En Linux / macOS:Bashpython3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
3. Configuración del FrontendBashcd frontend
npm install
cd ..
🔐 Variables de EntornoConfigura un archivo .env en el directorio raíz basándote en la siguiente plantilla:Ini, TOML# Base de Datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db

# Proveedores LLM
GROQ_API_KEY=gsk_tu_clave_de_groq
GEMINI_API_KEY=tu_clave_de_gemini

# WhatsApp Business (Meta Cloud API)
WHATSAPP_ACCESS_TOKEN=tu_token_de_meta
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_VERIFY_TOKEN=token_definido_para_el_webhook

# Seguridad y Sesiones
SECRET_KEY=clave_secreta_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
▶️ Ejecución Local1. Migraciones de Base de DatosAplica el historial de Alembic:Bashalembic -c backend/alembic.ini upgrade head
2. Iniciar Backend (FastAPI)Bashuvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
Swagger UI: http://localhost:8000/docsWebhook WhatsApp: http://localhost:8000/api/v1/whatsapp/webhook3. Iniciar Frontend (React)Bashcd frontend
npm run dev
Disponible en: http://localhost:51734. Conexión del Webhook con Meta (Túnel Ngrok)Bashngrok http 8000
Registra la URL generada ([https://xxxx.ngrok-free.app/api/v1/whatsapp/webhook](https://xxxx.ngrok-free.app/api/v1/whatsapp/webhook)) en el panel de configuración de WhatsApp dentro de Meta Developers.🧪 Pruebas y ValidaciónEl proyecto incluye scripts independientes en la raíz para validar integraciones de forma aislada:Bash# Validar inferencia y llamadas a función con Groq
python test_groq.py

# Validar conectividad con Google Gemini
python test_gemini.py

# Validar extracción y lectura de documentos PDF
python test_pdf.py

# Validar el pipeline RAG y búsqueda semántica
python test_rag.py
python test_search.py
📸 Capturas de Pantalla(Placeholders reservados para imágenes del repositorio)docs/images/dashboard.png - Panel de control y métricasdocs/images/excel_upload.png - Módulo de carga masiva de catálogosdocs/images/whatsapp_demo.png - Consultas y descuento de existencias por WhatsApp🗺️ Roadmap[x] Multi-tenancy lógico con aislamiento relacional por tenant_id.[x] Ingesta automática de inventarios Excel vía WhatsApp y API REST.[x] Registro y ejecución determinista de herramientas de stock y catálogo.[x] Embeddings locales con SentenceTransformers e integración RAG.[x] Autenticación JWT y modelos relacionales versionados con Alembic.[x] Frontend en React (Vite) para administración de asistentes y archivos.[ ] Ejecución atómica de venta contable y descuento de inventario en un único tool call.[ ] Suite formal de tests unitarios y de integración con pytest.[ ] Integración con la extensión pgvector en PostgreSQL para consultas vectoriales nativas.🔒 SeguridadFiltrado Multi-Tenant: Validación explícita del tenant_id en cada operación relacional para impedir accesos cruzados.Gestión Criptográfica de Claves: Hashing de contraseñas con bcrypt y verificación de firmas JWT.Saneamiento de Cargas Útiles: Validación estricta de tipos y formatos de entrada mediante Pydantic.Separación de Secretos: Configuración sensible gestionada mediante variables de entorno fuera del árbol de Git.👨‍💻 AutorJavier Andrés Estupiñán MéndezDesarrollador Backend Junior | Integración de IA & Automatización
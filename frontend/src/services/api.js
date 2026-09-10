const API_URL = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("token");
}

function getAuthHeaders(isJson = true) {
  const token = getToken();
  const headers = {};
  if (isJson) {
    headers["Content-Type"] = "application/json";
  }
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

// ==============================
// AUTH
// ==============================

export async function loginUser(data) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams(data),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Error al iniciar sesión");
  }
  return result;
}

export async function registerUser(data) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Error al registrarse");
  }
  return result;
}

// ==============================
// PROYECTOS
// ==============================

export async function getProjects() {
  const response = await fetch(`${API_URL}/proyectos`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Error al cargar los proyectos");
  }
  return result;
}

export async function createProject(data) {
  const response = await fetch(`${API_URL}/proyectos`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Error al crear el proyecto");
  }
  return result;
}

// ==============================
// ASISTENTES
// ==============================

export async function getAssistants(projectId) {
  const response = await fetch(`${API_URL}/asistentes/proyecto/${projectId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "No se pudieron cargar los asistentes");
  }
  return result;
}

export async function getAssistant(assistantId) {
  const response = await fetch(`${API_URL}/asistentes/${assistantId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "No se pudo obtener el asistente");
  }
  return result;
}

export async function createAssistant(projectId, data) {
  const response = await fetch(`${API_URL}/asistentes/proyecto/${projectId}`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(
      typeof result.detail === "string"
        ? result.detail
        : JSON.stringify(result.detail || result)
    );
  }
  return result;
}

export async function updateAssistant(assistantId, data) {
  const response = await fetch(`${API_URL}/asistentes/${assistantId}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Error al actualizar el asistente");
  }
  return result;
}

export async function deleteAssistant(assistantId) {
  const response = await fetch(`${API_URL}/asistentes/${assistantId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const result = await response.json().catch(() => ({}));
    throw new Error(result.detail || "Error al eliminar el asistente");
  }
  return true;
}

// ==============================
// CHAT
// ==============================

export async function sendChatMessage(assistantId, mensaje) {
  const response = await fetch(`${API_URL}/chat/${assistantId}`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({ mensaje }),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Error al enviar el mensaje");
  }
  return result; // Devuelve { respuesta: "..." }
}

// ==============================
// DOCUMENTOS
// ==============================

export async function getDocuments(projectId) {
  const response = await fetch(`${API_URL}/documentos/${projectId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Error al cargar documentos");
  }
  return result;
}

export async function uploadDocument(projectId, file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/documentos/${projectId}`, {
    method: "POST",
    headers: getAuthHeaders(false), // FormData no debe llevar Content-Type manual
    body: formData,
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.detail || "Error al subir el documento");
  }
  return result;
}

export async function deleteDocument(documentId) {
  const response = await fetch(`${API_URL}/documentos/${documentId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const result = await response.json().catch(() => ({}));
    throw new Error(result.detail || "Error al eliminar el documento");
  }
  return true;
}

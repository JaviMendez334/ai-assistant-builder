import React, { useState } from 'react';
import axios from 'axios';

const ExcelUploader = ({ tenantId = 1 }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResponse(null);
    setError(null);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Por favor selecciona un archivo Excel primero.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError(null);

    try {
      // Ajusta la URL base de tu backend FastAPI si es necesario
      const res = await axios.post(`http://localhost:8000/api/v1/importer/ingest/${tenantId}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResponse(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ocurrió un error al procesar el archivo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '24px', background: '#f9f9f9', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)', fontFamily: 'sans-serif' }}>
      <h2>📂 Importador Inteligente de Inventario y Cartera</h2>
      <p style={{ color: '#666', fontSize: '14px' }}>
        Sube tu archivo Excel (.xlsx o .xls). La inteligencia artificial detectará automáticamente las columnas y guardará la información.
      </p>

      <form onSubmit={handleUpload} style={{ marginTop: '20px' }}>
        <div style={{ border: '2px dashed #ccc', padding: '20px', textAlign: 'center', borderRadius: '8px', background: '#fff' }}>
          <input type="file" accept=".xlsx, .xls" onChange={handleFileChange} style={{ marginBottom: '10px' }} />
          {file && <p style={{ fontSize: '13px', color: '#333' }}>Archivo seleccionado: <strong>{file.name}</strong></p>}
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            marginTop: '16px',
            padding: '12px',
            background: loading ? '#ccc' : '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            fontSize: '16px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Procesando con IA y guardando...' : 'Subir e Importar Datos'}
        </button>
      </form>

      {error && (
        <div style={{ marginTop: '20px', padding: '12px', background: '#ffebee', color: '#c62828', borderRadius: '6px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {response && (
        <div style={{ marginTop: '20px', padding: '16px', background: '#e8f5e9', color: '#2e7d32', borderRadius: '6px' }}>
          <h3>¡Importación Exitosa!</h3>
          <p><strong>Archivo:</strong> {response.filename}</p>
          <p><strong>Tenant ID:</strong> {response.tenant_id}</p>
          <div style={{ marginTop: '10px', background: '#fff', padding: '10px', borderRadius: '4px', fontSize: '13px', color: '#333' }}>
            <pre>{JSON.stringify(response.results, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExcelUploader;
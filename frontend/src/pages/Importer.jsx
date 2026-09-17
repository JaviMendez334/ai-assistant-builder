import React from 'react';
import ExcelUploader from '../components/ExcelUploader';

const Importer = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h1>Importación de Datos</h1>
      <ExcelUploader tenantId={1} />
    </div>
  );
};

export default Importer;
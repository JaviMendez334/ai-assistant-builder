from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.services.excel_importer import inspect_excel, map_sheet_structure, process_and_save_excel

router = APIRouter(prefix="/api/v1/importer", tags=["Excel Importer"])

@router.post("/inspect")
async def inspect_uploaded_excel(file: UploadFile = File(...)):
    """Inspecciona y devuelve el mapeo sugerido sin guardar nada."""
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un Excel (.xlsx o .xls)"
        )
    
    contents = await file.read()
    summary = inspect_excel(contents)
    
    analysis = {}
    for sheet_name, data in summary.items():
        analysis[sheet_name] = {
            "summary": data,
            "ai_mapping": map_sheet_structure(sheet_name, data)
        }
        
    return {
        "filename": file.filename,
        "sheets_analyzed": len(analysis),
        "details": analysis
    }

@router.post("/ingest/{tenant_id}")
async def ingest_excel_data(
    tenant_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Procesa el Excel e inserta los datos directamente en la base de datos."""
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un Excel (.xlsx o .xls)"
        )

    contents = await file.read()
    try:
        report = process_and_save_excel(file_bytes=contents, tenant_id=tenant_id, db=db)
        return {
            "message": "Archivo procesado e importado con éxito",
            "filename": file.filename,
            "tenant_id": tenant_id,
            "results": report
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la importación: {str(e)}"
        )
    
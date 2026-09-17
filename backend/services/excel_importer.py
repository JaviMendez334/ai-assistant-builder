import io
import json
import pandas as pd
from sqlalchemy.orm import Session
from backend.services.llm_service import generar_respuesta
from backend.models.product import Product

def safe_int(value, default=0) -> int:
    """Convierte un valor a entero de forma segura, ignorando textos o nulos."""
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0) -> float:
    """Convierte un valor a decimal de forma segura."""
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def inspect_excel(file_bytes: bytes) -> dict:
    excel_buffer = io.BytesIO(file_bytes)
    excel_file = pd.ExcelFile(excel_buffer)
    sheets_summary = {}

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name).dropna(how="all")
        sample_records = df.head(3).to_dict(orient="records")
        sheets_summary[sheet_name] = {
            "columns": [str(col) for col in df.columns],
            "sample": sample_records,
            "total_rows": int(len(df))
        }
    return sheets_summary


def map_sheet_structure(sheet_name: str, sheet_data: dict) -> dict:
    prompt = f"""
Eres un analizador de bases de datos. Analiza la siguiente hoja de cálculo llamada '{sheet_name}':
- Columnas: {sheet_data['columns']}
- Muestra de datos: {json.dumps(sheet_data['sample'], default=str)}

Determina su categoría:
1. 'inventory' (si contiene productos, existencias, stock, precios o perfumes).
2. 'debts' (si contiene clientes, saldos, compras a crédito, abonos o deudas).
3. 'knowledge' (si es texto general, FAQs, políticas o notas).

Devuelve EXCLUSIVAMENTE un JSON válido con este formato:
{{
    "category": "inventory | debts | knowledge",
    "column_mapping": {{
        "standard_field": "nombre_columna_original"
    }}
}}

Campos estándar para 'inventory': name, price, stock, brand, sku, description.
Campos estándar para 'debts': customer_name, phone_number, total_debt, paid_amount, current_balance.
"""
    try:
        respuesta = generar_respuesta(
            messages=[{"role": "user", "content": prompt}],
            tools=None
        )
        raw_text = respuesta.choices[0].message.content
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        return {"category": "knowledge", "column_mapping": {}, "error": str(e)}


def process_and_save_excel(file_bytes: bytes, tenant_id: int, db: Session) -> dict:
    excel_buffer = io.BytesIO(file_bytes)
    excel_file = pd.ExcelFile(excel_buffer)
    results = {}

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name).dropna(how="all")
        if df.empty:
            continue

        sheet_summary = {
            "columns": [str(col) for col in df.columns],
            "sample": df.head(3).to_dict(orient="records")
        }
        mapping_info = map_sheet_structure(sheet_name, sheet_summary)
        category = mapping_info.get("category")
        col_map = mapping_info.get("column_mapping", {})

        inserted_count = 0

        if category == "inventory":
            for _, row in df.iterrows():
                product_data = {
                    "tenant_id": tenant_id,
                    "name": str(row.get(col_map.get("name", "name"), "Sin Nombre")),
                    "price": safe_float(row.get(col_map.get("price", "price"))),
                    "stock": safe_int(row.get(col_map.get("stock", "stock"))),
                    "brand": str(row.get(col_map.get("brand", "brand"), "")) if col_map.get("brand") else None,
                    "sku": str(row.get(col_map.get("sku", "sku"), "")) if col_map.get("sku") else None,
                    "description": str(row.get(col_map.get("description", "description"), "")) if col_map.get("description") else None,
                }
                new_product = Product(**product_data)
                db.add(new_product)
                inserted_count += 1

            db.commit()

        results[sheet_name] = {
            "category": category,
            "rows_processed": inserted_count,
            "status": "success"
        }

    return results

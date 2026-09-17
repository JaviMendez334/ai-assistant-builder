import io
import pandas as pd
from sqlalchemy.orm import Session
from backend.models.product import Product


def normalizar_texto(texto: str) -> str:
    return str(texto).strip().lower().replace("_", " ")


def procesar_excel_cartera(contenido_bytes: bytes, filename: str, tenant_id: int, db: Session) -> dict:
    """
    Lee el archivo Excel directamente desde memoria, identifica las columnas clave
    y actualiza o inserta los productos/inventario aislados por tenant_id.
    """
    try:
        # Cargar el Excel en un DataFrame usando BytesIO sin tocar el disco
        df = pd.read_excel(io.BytesIO(contenido_bytes))

        if df.empty:
            return {
                "success": False,
                "message": f"El archivo *{filename}* está vacío."
            }

        # Normalizar nombres de columnas a minúsculas
        columnas_originales = df.columns.tolist()
        df.columns = [normalizar_texto(c) for c in df.columns]

        # Detección inteligente de columnas por palabras clave
        col_nombre = next(
            (c for c in df.columns if any(k in c for k in ["producto", "articulo", "item", "nombre", "cliente", "descripcion"])), 
            None
        )
        col_precio = next(
            (c for c in df.columns if any(k in c for k in ["precio", "valor", "monto", "saldo", "deuda", "total", "costo"])), 
            None
        )
        col_stock = next(
            (c for c in df.columns if any(k in c for k in ["stock", "cantidad", "cant", "unidades", "disponible"])), 
            None
        )
        col_marca = next(
            (c for c in df.columns if any(k in c for k in ["marca", "brand", "linea", "categoria"])), 
            None
        )

        if not col_nombre or not col_precio:
            return {
                "success": False,
                "message": (
                    f"⚠️ No pude identificar las columnas clave en *{filename}*.\n\n"
                    f"Columnas detectadas: `{', '.join(columnas_originales)}`\n"
                    f"Asegúrate de incluir al menos una columna para el **Nombre/Producto** y otra para el **Precio/Valor**."
                )
            }

        registros_procesados = 0

        for _, fila in df.iterrows():
            nombre = str(fila[col_nombre]).strip()
            if not nombre or nombre.lower() == "nan":
                continue

            # Limpiar valor numérico (moneda, separadores de miles y decimales)
            try:
                valor_crudo = str(fila[col_precio]).replace("$", "").replace(".", "").replace(",", ".").strip()
                precio_val = float(valor_crudo)
            except (ValueError, TypeError):
                precio_val = 0.0

            # Limpiar stock si existe
            stock_val = 0
            if col_stock:
                try:
                    stock_crudo = str(fila[col_stock]).replace(",", ".").strip()
                    stock_val = int(float(stock_crudo))
                except (ValueError, TypeError):
                    stock_val = 0

            marca_val = str(fila.get(col_marca, "")).strip() if col_marca else None
            if marca_val and marca_val.lower() == "nan":
                marca_val = None

            # -----------------------------------------------------------------
            # UPSERT AISLADO POR TENANT_ID
            # -----------------------------------------------------------------
            producto_existente = (
                db.query(Product)
                .filter(
                    Product.tenant_id == tenant_id,
                    Product.name.ilike(nombre)
                )
                .first()
            )

            if producto_existente:
                producto_existente.price = precio_val
                if col_stock:
                    producto_existente.stock = stock_val
                if marca_val:
                    producto_existente.brand = marca_val
            else:
                nuevo_producto = Product(
                    tenant_id=tenant_id,
                    name=nombre,
                    price=precio_val,
                    stock=stock_val,
                    brand=marca_val
                )
                db.add(nuevo_producto)

            registros_procesados += 1

        db.commit()

        return {
            "success": True,
            "registros": registros_procesados,
            "message": (
                f"✅ Archivo *{filename}* procesado con éxito.\n\n"
                f"📊 **Registros sincronizados:** {registros_procesados}\n"
                f"🏢 **Tenant ID:** {tenant_id}\n\n"
                f"El inventario y precios ya están disponibles para consultas en WhatsApp."
            )
        }

    except Exception as e:
        db.rollback()
        print(f"❌ Error parseando Excel: {e}")
        return {
            "success": False,
            "message": f"❌ Ocurrió un error al leer la estructura de *{filename}*: {str(e)}"
        }
from sqlalchemy.orm import Session
from backend.models.product import Product


def search_products(query: str = "", tenant_id: int = None, db: Session = None) -> dict:
    """
    Busca productos en el catálogo/inventario de la empresa filtrando por tenant_id.
    Si query está vacío, lista los productos disponibles.
    """
    if not tenant_id or not db:
        return {"success": False, "error": "Falta tenant_id o sesión de base de datos."}

    consulta = db.query(Product).filter(Product.tenant_id == tenant_id)

    if query and query.strip():
        termino = f"%{query.strip()}%"
        consulta = consulta.filter(
            (Product.name.ilike(termino)) | 
            (Product.brand.ilike(termino)) |
            (Product.description.ilike(termino))
        )

    # Limitar a los primeros 15 resultados para no saturar el contexto
    productos = consulta.limit(15).all()

    if not productos:
        return {
            "success": True,
            "count": 0,
            "message": f"No se encontraron productos en el inventario que coincidan con '{query}'."
        }

    items = []
    for p in productos:
        items.append({
            "id": p.id,
            "nombre": p.name,
            "precio": float(p.price) if p.price else 0.0,
            "stock": p.stock,
            "marca": p.brand or "N/A"
        })

    return {
        "success": True,
        "count": len(items),
        "productos": items
    }
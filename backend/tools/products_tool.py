from backend.database.session import SessionLocal
from backend.models.product import Product
from backend.tools.registry import registry


class SearchProductsTool:
    name = "search_products"

    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Consulta el inventario y catálogo de productos de la empresa: nombres, precios y stock disponible.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Nombre, tipo o término de búsqueda (ej: 'pijama', 'satinada'). Deja vacío para ver todo el inventario."
                        }
                    },
                    "required": []
                }
            }
        }

    def execute(self, query: str = "", tenant_id: int = None, **kwargs):
        if not tenant_id:
            return {"error": "tenant_id es requerido para consultar productos."}

        db = SessionLocal()
        try:
            consulta = db.query(Product).filter(Product.tenant_id == tenant_id)

            if query and query.strip():
                filtro = f"%{query.strip()}%"
                consulta = consulta.filter(
                    (Product.name.ilike(filtro)) |
                    (Product.brand.ilike(filtro))
                )

            productos = consulta.limit(20).all()

            if not productos:
                return {"encontrados": 0, "mensaje": f"No hay productos que coincidan con '{query}'."}

            resultado = []
            for p in productos:
                resultado.append({
                    "nombre": p.name,
                    "precio": float(p.price) if p.price else 0.0,
                    "stock": p.stock,
                    "marca": p.brand or "N/A"
                })

            return {
                "encontrados": len(resultado),
                "productos": resultado
            }
        finally:
            db.close()


# Auto-registro en el sistema
registry.register(SearchProductsTool())
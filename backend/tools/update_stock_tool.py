from typing import Any
from backend.database.session import SessionLocal
from backend.models.product import Product
from backend.tools.registry import registry


class UpdateStockTool:
    name = "update_product_stock"
    description = (
        "Actualiza el inventario/stock de un producto en la base de datos de la empresa. "
        "Permite restar unidades (por venta o salida), sumar (por reposición o devolución) "
        "o fijar el valor total exacto de stock."
    )

    def schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "producto": {
                            "type": "string",
                            "description": "Nombre del producto a actualizar.",
                        },
                        "cantidad": {
                            "type": "integer",
                            "description": "Cantidad de unidades a descontar, sumar o establecer.",
                        },
                        "operacion": {
                            "type": "string",
                            "enum": ["restar", "sumar", "fijar"],
                            "description": "Operación a realizar: 'restar' para ventas/salidas, 'sumar' para entradas, 'fijar' para asignar un stock exacto.",
                        },
                    },
                    "required": ["producto", "cantidad", "operacion"],
                },
            },
        }

    def execute(self, producto: str, cantidad: int, operacion: str, tenant_id: int, **kwargs: Any) -> dict[str, Any]:
        db = SessionLocal()
        try:
            # Buscar el producto asegurando el aislamiento por empresa
            prod = (
                db.query(Product)
                .filter(Product.tenant_id == tenant_id)
                .filter(Product.name.ilike(f"%{producto.strip()}%"))
                .first()
            )

            if not prod:
                return {
                    "success": False,
                    "mensaje": f"No se encontró el producto '{producto}' en el inventario de esta empresa."
                }

            stock_anterior = prod.stock or 0

            if operacion == "restar":
                if stock_anterior < cantidad:
                    return {
                        "success": False,
                        "mensaje": f"Stock insuficiente para '{prod.name}'. Solo quedan {stock_anterior} unidades disponibles."
                    }
                prod.stock = stock_anterior - cantidad

            elif operacion == "sumar":
                prod.stock = stock_anterior + cantidad

            elif operacion == "fijar":
                prod.stock = cantidad

            db.commit()
            db.refresh(prod)

            return {
                "success": True,
                "producto": prod.name,
                "stock_anterior": stock_anterior,
                "nuevo_stock": prod.stock,
                "mensaje": f"Stock de '{prod.name}' actualizado exitosamente de {stock_anterior} a {prod.stock}."
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()


registry.register(UpdateStockTool())

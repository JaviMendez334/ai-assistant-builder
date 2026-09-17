"""
Paquete de herramientas.
"""

from backend.tools.registry import registry

# Solo importa la herramienta de productos que acabamos de crear
import backend.tools.products_tool
import backend.tools.update_stock_tool
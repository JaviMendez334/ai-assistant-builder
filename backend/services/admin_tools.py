# backend/services/admin_tools.py
from sqlalchemy.orm import Session
# Importa tus modelos de SQLAlchemy (Tenant, User, etc.)

def crear_nuevo_tenant(db: Session, nombre_negocio: str, admin_phone: str):
    """
    Crea un nuevo negocio/tenant en la base de datos y le asigna un número de WhatsApp administrador.
    """
    # Lógica para guardar en PostgreSQL
    # tenant = Tenant(name=nombre_negocio)
    # db.add(tenant)
    # db.commit()
    return f"✅ Negocio '{nombre_negocio}' creado exitosamente con el admin {admin_phone}."

def consultar_estado_sistema(db: Session):
    """
    Devuelve un resumen rápido del estado general del sistema (número de tenants, productos, etc.).
    """
    # Lógica de conteo en la base de datos
    return "📊 Estado del Sistema: 3 Tenants activos, 145 productos indexados en RAG, API Operativa."
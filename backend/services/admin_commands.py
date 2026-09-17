import json
from sqlalchemy.orm import Session

from backend.models.tenant import Tenant
from backend.models.product import Product
from backend.services.llm_service import generar_respuesta


def procesar_comando_super_admin(message_text: str, db: Session) -> str:
    """
    Procesa consultas y comandos del Super Admin utilizando el motor LLM unificado
    y métricas globales de la base de datos.
    """
    texto_lower = message_text.lower().strip()

    # 1. Comandos directos rápidos: Listar empresas registradas
    if any(k in texto_lower for k in ["listar", "empresas", "negocios", "quienes", "cuáles", "cuantas"]):
        tenants = db.query(Tenant).all()
        if not tenants:
            return (
                "📋 No hay negocios registrados en la base de datos todavía. "
                "Puedes decirme algo como: *'Registra una nueva tienda llamada ModaReal con el número 573001234567'*."
            )

        lista = "📋 *Negocios Registrados en el Sistema*:\n\n"
        for t in tenants:
            total_prods = db.query(Product).filter(Product.tenant_id == t.id).count()
            lista += f"🏢 *{t.name}*\n📞 Tel: {t.phone}\n🆔 ID: {t.id}\n📦 Productos: {total_prods}\n------------------\n"
        return lista

    # 2. Comandos directos rápidos: Estado o resumen general
    if any(k in texto_lower for k in ["estado", "resumen", "cómo va", "status"]):
        total_t = db.query(Tenant).count()
        total_p = db.query(Product).count()
        return (
            f"📊 *Estado del Sistema*:\n"
            f"• Servidor y Base de Datos: 🟢 Operativos\n"
            f"• Total de negocios activos: {total_t}\n"
            f"• Total de productos cargados: {total_p}\n"
            f"• Canal de WhatsApp: 🟢 Sincronizado"
        )

    # 3. Consultas generales o registro de empresas vía LLM centralizado
    total_tenants = db.query(Tenant).count()
    tenants = db.query(Tenant).all()
    lista_tenants = ", ".join([f"{t.name} (ID: {t.id})" for t in tenants])
    total_productos = db.query(Product).count()

    prompt_sistema = f"""
Eres el asistente ejecutivo del Super Administrador de la plataforma.
Acceso a datos globales actuales:
- Total de empresas (Tenants) registradas: {total_tenants}
- Empresas activas: {lista_tenants}
- Total de productos cargados en el sistema: {total_productos}

Tu tarea:
1. Si el usuario solicita registrar, dar de alta o crear una empresa/negocio, responde EXCLUSIVAMENTE con este JSON:
   {{"accion": "crear", "nombre": "NombreNegocio", "telefono": "NumeroTelefono"}}
   (El teléfono debe contener solo dígitos e indicativo de país).
2. Para cualquier otra pregunta (ej: '¿alguna empresa subió archivos?', métricas, dudas), responde en lenguaje natural claro, conciso y directo basándote en los datos del sistema.
"""

    messages = [
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": message_text}
    ]

    try:
        respuesta = generar_respuesta(messages=messages, tools=None)
        if not respuesta or not respuesta.choices:
            return "No pude generar una respuesta en este momento."

        contenido = respuesta.choices[0].message.content.strip()

        # Detección de creación de empresa vía JSON
        if "{" in contenido and "crear" in contenido:
            try:
                inicio = contenido.find("{")
                fin = contenido.rfind("}") + 1
                datos = json.loads(contenido[inicio:fin])

                if datos.get("accion") == "crear":
                    nombre = datos.get("nombre")
                    telefono = datos.get("telefono")

                    if not nombre or not telefono:
                        return "🤔 Entendí que deseas registrar un negocio, pero faltó claridad en el nombre o el teléfono. ¿Podrías indicármelos de nuevo?"

                    telefono_limpio = str(telefono).replace("+", "").strip()

                    # Validar duplicados
                    existe = db.query(Tenant).filter(
                        (Tenant.name == nombre) | (Tenant.phone == telefono_limpio)
                    ).first()
                    if existe:
                        return f"⚠️ El negocio *{nombre}* o el teléfono *{telefono_limpio}* ya se encuentran registrados."

                    # Prompt administrativo base para el nuevo tenant
                    prompt_base = (
                        f"Eres el asistente administrativo y operativo exclusivo para el dueño/administrador de {nombre}. "
                        f"Tu labor principal es asistir a la administración en la gestión interna de su tienda: "
                        f"consultar inventario y disponibilidad, registrar abonos y compras de clientes, "
                        f"verificar deudas y cartera pendiente. Mantén un tono profesional, directo y eficiente."
                    )

                    nuevo_tenant = Tenant(
                        name=nombre,
                        phone=telefono_limpio,
                        system_prompt=prompt_base,
                    )
                    db.add(nuevo_tenant)
                    db.commit()
                    db.refresh(nuevo_tenant)

                    return (
                        f"✅ ¡Negocio registrado con éxito!\n\n"
                        f"🏢 *{nuevo_tenant.name}*\n"
                        f"📞 Teléfono: {nuevo_tenant.phone}\n"
                        f"🆔 ID en Base de Datos: {nuevo_tenant.id}\n"
                        f"📋 Rol: Copiloto Administrativo auto-configurado\n\n"
                        f"🚀 Ya puede escribirte por WhatsApp para gestionar su negocio."
                    )
            except Exception:
                pass  # Si no era un JSON de creación, entrega el texto normal del LLM

        return contenido

    except Exception as e:
        print(f"❌ Error procesando IA para admin: {e}")
        return f"Ocurrió un error consultando el asistente administrativo: {str(e)}"
    
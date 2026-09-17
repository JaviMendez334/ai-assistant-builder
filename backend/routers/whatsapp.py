import httpx
from fastapi import APIRouter, Request, Response, Query, HTTPException, status, Depends
from sqlalchemy.orm import Session

# Importar base de datos y modelos
from backend.database.session import get_db
from backend.models.tenant import Tenant

# Importar servicios
from backend.services.excel_service import procesar_excel_cartera
from backend.services.ai_engine import responder
from backend.services.admin_commands import procesar_comando_super_admin
from backend.services.llm_service import generar_respuesta

router = APIRouter(prefix="/api/v1/whatsapp", tags=["WhatsApp"])

VERIFY_TOKEN = "Aura2332"
ACCESS_TOKEN = "EAAW5t8YYxw8BShV7DK8982ZA00IuZBry2DmTbf7ASXAMWRzDVVllVVIhKuDLZA8qezjg9lwxq1ED7eVsAm8LKzH7QZA10JZCFub1KwMOw47WWMYDZARKQZCpsZCZB8W0B6TjhVBGEgimT5JAfGZAGjmA39C2PK6bWv7K2MI0oZAy1QzOJypZCJpDnFHZAAJ7L9GBZC3Su5OfoFInjy67Y1qkaSjIlZAUNWMzq5XtPVf2teBXXZA4gJhGaQvm0RCBv7tD6AbKyXQPn00fDjkSIsaBGWZBZAtFVB"  # Tu token actual de Meta Developers
PHONE_NUMBER_ID = "1281170051748886"

# Tu número personal configurado como Super Admin
SUPER_ADMIN_PHONE = "573105419439" 
DEFAULT_CONVERSATION_ID = 1


# 1. Verificación del Webhook (GET)
@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return Response(content=str(hub_challenge), media_type="text/plain")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token no coincide")


# 2. Envío de mensajes a través de Graph API
async def send_whatsapp_message(to_number: str, text: str):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {"body": text},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        return response.json()


# =========================================================================
# FUNCIÓN DE DESCARGA DE MEDIOS (Graph API)
# =========================================================================
async def descargar_archivo_meta(media_id: str) -> bytes:
    """
    Obtiene la URL temporal del archivo en Meta Graph API y descarga su contenido binario.
    """
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        meta_url = f"https://graph.facebook.com/v22.0/{media_id}"
        res_meta = await client.get(meta_url, headers=headers)
        if res_meta.status_code != 200:
            raise Exception(f"Error consultando media_id en Meta: {res_meta.text}")

        direct_download_url = res_meta.json().get("url")
        if not direct_download_url:
            raise Exception("No se encontró la URL de descarga en la respuesta de Meta.")

        res_file = await client.get(direct_download_url, headers=headers)
        if res_file.status_code != 200:
            raise Exception(f"Error descargando el archivo binario: {res_file.status_code}")

        return res_file.content


# =========================================================================
# 3. Receptor de mensajes (POST) con ruteo, documentos y aislamiento de Tenant
# =========================================================================
@router.post("/webhook")
async def receive_whatsapp_message(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if messages:
            message = messages[0]
            sender_phone = message.get("from")  # Quien escribe
            message_type = message.get("type")

            reply_text = ""

            # =========================================================================
            # CASO A: RECEPCIÓN DE DOCUMENTOS (Excel, CSV, PDF)
            # =========================================================================
            if message_type == "document":
                doc_info = message.get("document", {})
                media_id = doc_info.get("id")
                filename = doc_info.get("filename", "archivo_desconocido")
                mime_type = doc_info.get("mime_type", "")

                print(f"📎 Documento recibido de {sender_phone}: {filename} (ID: {media_id})")

                # Verificar si quien envía el archivo es una empresa registrada
                tenant_empresa = db.query(Tenant).filter(Tenant.phone == sender_phone).first()

                if tenant_empresa:
                    try:
                        contenido_bytes = await descargar_archivo_meta(media_id)
                        print(f"✅ Archivo {filename} descargado con éxito ({len(contenido_bytes)} bytes)")

                        # Validación y procesamiento del archivo
                        if filename.lower().endswith((".xlsx", ".xls")):
                            resultado = procesar_excel_cartera(
                                contenido_bytes=contenido_bytes,
                                filename=filename,
                                tenant_id=tenant_empresa.id,
                                db=db
                            )
                            reply_text = resultado["message"]
                        else:
                            reply_text = f"📄 Recibí *{filename}*, pero por ahora el sistema solo procesa archivos Excel (`.xlsx` o `.xls`)."

                    except Exception as err:
                        print(f"❌ Error descargando/procesando archivo: {err}")
                        reply_text = f"⚠️ Ocurrió un problema al procesar el archivo *{filename}*."
                else:
                    reply_text = "⚠️ Solo las empresas registradas pueden subir archivos de gestión al sistema."

                api_response = await send_whatsapp_message(sender_phone, reply_text)
                print(f"📤 Respuesta enviada a {sender_phone}: {api_response}")
                return Response(status_code=status.HTTP_200_OK)

            # =========================================================================
            # CASO B: MENSAJES DE TEXTO CONVENCIONALES
            # =========================================================================
            message_text = None
            if message_type == "text":
                message_text = message.get("text", {}).get("body")

            print(f"📩 Mensaje recibido de {sender_phone}: {message_text}")

            if message_text and sender_phone:
                # 1. NIVEL SUPER ADMIN
                if sender_phone == SUPER_ADMIN_PHONE:
                    print("👑 Detectado comando de Super Admin")
                    reply_text = procesar_comando_super_admin(message_text, db)

                # 2 y 3. NIVELES DE EMPRESA Y CLIENTES EXTERNOS
                else:
                    tenant_empresa = db.query(Tenant).filter(Tenant.phone == sender_phone).first()

                    # NIVEL 2: Dueño de la Empresa
                    if tenant_empresa:
                        print(f"🏢 Dueño de Empresa interactuando: {tenant_empresa.name} (Tenant ID: {tenant_empresa.id})")
                        reply_text = responder(
                            conversation_id=tenant_empresa.id,
                            pregunta=message_text,
                            tenant_id=tenant_empresa.id
                        )

                    # NIVEL 3: Cliente externo
                    else:
                        print(f"👤 Cliente externo interactuando desde: {sender_phone}")
                        reply_text = responder(
                            conversation_id=DEFAULT_CONVERSATION_ID,
                            pregunta=message_text,
                            tenant_id=None
                        )

                # Enviar respuesta al remitente
                api_response = await send_whatsapp_message(sender_phone, reply_text)
                print(f"📤 Respuesta enviada a {sender_phone}: {api_response}")

    except Exception as e:
        print(f"❌ Error procesando webhook: {e}")

    return Response(status_code=status.HTTP_200_OK)
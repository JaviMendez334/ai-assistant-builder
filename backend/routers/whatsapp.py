import httpx
from fastapi import APIRouter, Request, Response, Query, HTTPException, status

# Importar el motor de IA
from backend.services.ai_engine import responder

router = APIRouter(prefix="/api/v1/whatsapp", tags=["WhatsApp"])

VERIFY_TOKEN = "Aura2332"
# Pega tu token de Meta Developers aquí
ACCESS_TOKEN = "EAAW5t8YYxw8BSTkey8HvVU2p60IouYoLpPuPNJ5NIx5R1usZBf8S1u0UFSUZC8hIqKwWetSGBN4TezATMEpEk86yf2DnpLZAVa7Mf1IPY0ZCKCwW8zXgVwAvQmYSfPiMW6T21WJD1JZBUjygZCuvYjxStNP1zcNsnL76wTaAALnd1PKd0tQazNZCq0MyilmZCfCBjaoWXL2YUFcfgecZBeeEwMJZBi8LCHDLmpzsS3s217gboUFjV0utGryk6sRZCdSeMrcDK2ijbn6YZCbKqaRe3ZBcp"
PHONE_NUMBER_ID = "1281170051748886"

# Número de prueba verificado
DEV_TEST_PHONE = "573105419439"

# ID de conversación por defecto para cargar contexto/instrucciones del asistente
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


# 3. Receptor de mensajes (POST) y ejecución del motor IA
@router.post("/webhook")
async def receive_whatsapp_message(request: Request):
    data = await request.json()

    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if messages:
            message = messages[0]

            # Extraer el texto del mensaje
            message_text = None
            if message.get("type") == "text":
                message_text = message.get("text", {}).get("body")

            print(f"📩 Mensaje recibido de WhatsApp: {message_text}")

            if message_text:
                # 1. Generar la respuesta usando el motor de IA con RAG y Tools
                ai_reply = responder(
                    conversation_id=DEFAULT_CONVERSATION_ID,
                    pregunta=message_text
                )
                print(f"🤖 Respuesta generada por IA:\n{ai_reply}")

                # 2. Enviar la respuesta generada al WhatsApp
                api_response = await send_whatsapp_message(DEV_TEST_PHONE, ai_reply)
                print(f"📤 Respuesta de Meta API: {api_response}")

    except Exception as e:
        print(f"❌ Error procesando webhook: {e}")

    return Response(status_code=status.HTTP_200_OK)

import json

from backend.services.conversation_service import (
    obtener_historial,
    obtener_instrucciones,
    obtener_assistant_id,
)

from backend.services.llm_service import generar_respuesta

from backend.tools.executor import (
    execute_tool,
    get_available_tools,
)


def responder(
    conversation_id: int,
    pregunta: str,
):
    historial = obtener_historial(
        conversation_id
    )

    instrucciones = obtener_instrucciones(
        conversation_id
    )

    instrucciones_rag = f"""
{instrucciones}

REGLAS DE CONOCIMIENTO:

1. Cuando la pregunta pueda ser respondida utilizando
   información contenida en los documentos del asistente,
   DEBES utilizar la herramienta search_documents.

2. No inventes información.

3. Después de utilizar search_documents, debes analizar
   cuidadosamente la información recuperada.

4. Si la información recuperada responde la pregunta,
   utiliza esa información para construir la respuesta.

5. NO debes utilizar search_documents repetidamente para
   la misma pregunta si la primera búsqueda ya recuperó
   información relevante.

6. Diferencia claramente entre:

   - información explícitamente presente en los documentos;
   - información que puede inferirse razonablemente;
   - información que NO está disponible.

7. Si el documento contiene una cantidad concreta de
   elementos, puedes informar esa cantidad siempre que
   aclares su alcance.

8. Por ejemplo, si el documento contiene una sección llamada
   "Matriz de SKUs Representativos" y aparecen:

   - SKU-HOOD-001
   - SKU-JEAN-002
   - SKU-TEE-003

   puedes decir que existen 3 SKUs representativos
   documentados.

   Sin embargo, NO debes afirmar que el catálogo completo
   contiene solamente 3 productos si el documento no lo dice.

99. Si el documento contiene una lista o matriz de productos
   representativos y la pregunta pregunta cuántos productos hay,
   debes informar primero cuántos productos representativos aparecen
   en la documentación.

10. Si esos productos están identificados mediante SKU, menciona
    los SKU encontrados cuando sea útil.

11. NO confundas la cantidad de productos representativos
    documentados con el total del catálogo.

12. Si el documento contiene 3 SKUs representativos pero no indica
    el total del catálogo, responde por ejemplo:

    "La documentación muestra 3 SKUs representativos: SKU-HOOD-001,
    SKU-JEAN-002 y SKU-TEE-003. Sin embargo, el documento no indica
    cuántos productos tiene el catálogo completo."

13. Nunca respondas simplemente que "no se indica cuántos productos
    hay" cuando sí existe una cantidad concreta de productos
    representativos dentro de la información recuperada.

La herramienta search_documents recibe:

- question: la pregunta que debe buscarse.

NO envíes conversation_id dentro de los argumentos.
El sistema lo agrega automáticamente.
"""

    messages = [
        {
            "role": "system",
            "content": instrucciones_rag,
        },
        {
            "role": "system",
            "content": historial,
        },
        {
            "role": "user",
            "content": pregunta,
        },
    ]

    assistant_id = obtener_assistant_id(
        conversation_id
    )

    tools = get_available_tools(
        assistant_id
    )

    print("\n========== AI ENGINE ==========")
    print("Pregunta:", pregunta)
    print("Conversation ID:", conversation_id)
    print("Assistant ID:", assistant_id)

    print("\nHerramientas disponibles:")

    for tool in tools:
        print(
            "-",
            tool["function"]["name"],
        )

    # ============================================================
    # PRIMERA LLAMADA AL LLM
    # ============================================================

    print(
        "\n========== RONDA LLM 1 =========="
    )

    respuesta = generar_respuesta(
        messages=messages,
        tools=tools,
    )

    if respuesta is None:
        print(
            "❌ generar_respuesta devolvió None"
        )

        return (
            "No pude generar una respuesta "
            "en este momento."
        )

    mensaje = respuesta.choices[0].message

    print(
        "Contenido:",
        mensaje.content,
    )

    print(
        "Tool calls:",
        mensaje.tool_calls,
    )

    # ============================================================
    # EL MODELO RESPONDIÓ SIN HERRAMIENTAS
    # ============================================================

    if not mensaje.tool_calls:

        print(
            "✅ El modelo respondió directamente."
        )

        if mensaje.content:
            return mensaje.content

        return (
            "No pude generar una respuesta "
            "en este momento."
        )

    # ============================================================
    # EL MODELO SOLICITÓ UNA HERRAMIENTA
    # ============================================================

    messages.append(mensaje)

    for tool_call in mensaje.tool_calls:

        nombre_herramienta = (
            tool_call.function.name
        )

        print(
            "\n========== TOOL =========="
        )

        print(
            "Herramienta:",
            nombre_herramienta,
        )

        # --------------------------------------------------------
        # Interpretar argumentos
        # --------------------------------------------------------

        try:

            argumentos = json.loads(
                tool_call.function.arguments
            )

        except json.JSONDecodeError:

            print(
                "❌ JSON inválido:",
                tool_call.function.arguments,
            )

            resultado = {
                "success": False,
                "error": (
                    "Los argumentos de la herramienta "
                    "no tienen un JSON válido."
                ),
            }

        else:

            # El backend agrega conversation_id.
            argumentos.setdefault(
                "conversation_id",
                conversation_id,
            )

            print(
                "Argumentos:",
                argumentos,
            )

            # ----------------------------------------------------
            # Ejecutar herramienta
            # ----------------------------------------------------

            try:

                resultado = execute_tool(
                    nombre_herramienta,
                    argumentos,
                )

            except Exception as e:

                print(
                    "❌ Error ejecutando herramienta:",
                    str(e),
                )

                resultado = {
                    "success": False,
                    "tool": nombre_herramienta,
                    "error": str(e),
                }

            print(
                "Resultado:",
                resultado,
            )

        # --------------------------------------------------------
        # Enviar resultado al LLM
        # --------------------------------------------------------

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    resultado,
                    ensure_ascii=False,
                ),
            }
        )

    # ============================================================
    # RESPUESTA FINAL
    #
    # IMPORTANTE:
    # tools=None evita que el modelo vuelva a llamar
    # search_documents.
    # ============================================================

    messages.append(
        {
            "role": "system",
            "content": """
Ya ejecutaste las herramientas necesarias.

Ahora debes responder al usuario utilizando
ÚNICAMENTE la información disponible en el historial
y el resultado de las herramientas que acabas de recibir.

NO puedes utilizar ninguna herramienta adicional.

Si la información recuperada no permite responder
exactamente la pregunta, dilo claramente.

No inventes datos.

Si solamente se encontraron ejemplos o elementos
representativos, no los presentes como el total general.
""",
        }
    )

    print(
        "\n========== RESPUESTA FINAL =========="
    )

    respuesta_final = generar_respuesta(
        messages=messages,
        tools=None,
    )

    if respuesta_final is None:

        print(
            "❌ La respuesta final devolvió None"
        )

        return (
            "No pude generar una respuesta "
            "en este momento."
        )

    mensaje_final = (
        respuesta_final
        .choices[0]
        .message
    )

    print(
        "Contenido:",
        mensaje_final.content,
    )

    if mensaje_final.content:
        return mensaje_final.content

    return (
        "No pude generar una respuesta "
        "en este momento."
    )

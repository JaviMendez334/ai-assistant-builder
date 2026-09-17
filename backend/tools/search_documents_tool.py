from backend.services.search_service import (
    buscar_chunks,
)

from backend.tools.base import BaseTool


class SearchDocumentsTool(
    BaseTool
):

    name = "search_documents"

    description = (
        "Busca información dentro de los "
        "documentos del asistente. Debes "
        "usar esta herramienta cuando el "
        "usuario pregunte sobre información "
        "que pueda estar contenida en los "
        "documentos."
    )

    def execute(
        self,
        question: str,
        conversation_id: int,
        tenant_id: int | None = None,
        **kwargs,
    ):

        resultados = buscar_chunks(
            pregunta=question,
            conversation_id=conversation_id,
            tenant_id=tenant_id,
        )

        if not resultados:

            return {
                "documents": []
            }

        return {
            "documents": [
                item["chunk"]
                for item in resultados
            ]
        }

    def schema(self):

        return {
            "type": "function",

            "function": {
                "name": self.name,

                "description": self.description,

                "parameters": {
                    "type": "object",

                    "properties": {
                        "question": {
                            "type": "string",

                            "description": (
                                "La pregunta que "
                                "debe buscarse "
                                "en los documentos."
                            ),
                        },
                    },

                    "required": [
                        "question"
                    ],

                    "additionalProperties": False,
                },
            },
        }
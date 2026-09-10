from backend.tools.base import BaseTool

from backend.services.search_service import buscar_chunks


class SearchDocumentsTool(BaseTool):

    name = "search_documents"

    description = (
        "Busca información dentro de los documentos del proyecto."
    )

    def execute(
        self,
        question: str,
        conversation_id: int,
    ):

        resultados = buscar_chunks(
            question,
            conversation_id,
        )

        return resultados

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
                            "description": "Pregunta del usuario."
                        },
                        "conversation_id": {
                            "type": "integer",
                            "description": "Conversación actual."
                        },
                    },
                    "required": [
                        "question",
                        "conversation_id",
                    ],
                },
            },
        }
    
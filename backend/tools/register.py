from backend.tools.registry import registry

from backend.tools.builtins.search_documents import SearchDocumentsTool


registry.register(
    SearchDocumentsTool()
)


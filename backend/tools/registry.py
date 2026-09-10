from backend.tools.registry_class import ToolRegistry

from backend.tools.search_documents_tool import (
    SearchDocumentsTool,
)

registry = ToolRegistry()

registry.register(
    SearchDocumentsTool()
)

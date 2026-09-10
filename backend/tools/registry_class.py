from backend.tools.base import BaseTool


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get(self, name: str):
        return self.tools.get(name)

    def all(self):
        return list(self.tools.values())

    def schemas(self):
        return [
            tool.schema()
            for tool in self.tools.values()
        ]

    def schemas_for(self, tool_names: list[str]):
        return [
            self.tools[name].schema()
            for name in tool_names
            if name in self.tools
        ]
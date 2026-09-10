from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Clase base para todas las herramientas
    que podrá utilizar el asistente IA.
    """

    name: str = ""
    description: str = ""


    @abstractmethod
    def execute(self, **kwargs):
        """
        Lógica que ejecuta la herramienta.
        """
        pass


    @abstractmethod
    def schema(self):
        """
        Esquema compatible con function calling
        de modelos como Groq/OpenAI.
        """
        pass
    
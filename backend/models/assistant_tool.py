from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from backend.database.database import Base


class AssistantTool(Base):
    __tablename__ = "assistant_tools"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    assistant_id = Column(
        Integer,
        ForeignKey(
            "assistants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    tool_name = Column(
        String(100),
        nullable=False,
    )

    activo = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    __table_args__ = (
        UniqueConstraint(
            "assistant_id",
            "tool_name",
            name="uq_assistant_tool",
        ),
    )
    
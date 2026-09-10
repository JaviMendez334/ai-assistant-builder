from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from backend.database.database import Base


class Assistant(Base):

    __tablename__ = "assistants"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(
        String(100),
        nullable=False,
    )

    instrucciones = Column(
        Text,
        nullable=False,
    )

    modelo = Column(
        String(100),
        nullable=False,
        server_default="gpt-4.1-mini",
    )

    activo = Column(
        Integer,
        nullable=False,
        server_default="1",
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    
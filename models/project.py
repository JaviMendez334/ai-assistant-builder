from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from database.database import Base

from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    descripcion = Column(Text, nullable=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    documents = relationship(
        "Document",
        back_populates="project",
        cascade="all, delete"
    )
    
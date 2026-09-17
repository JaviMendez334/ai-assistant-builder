from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB

from backend.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer, 
        ForeignKey("tenants.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    name = Column(String(255), nullable=False, index=True)
    brand = Column(String(100), nullable=True)
    price = Column(Numeric(12, 2), nullable=False, default=0.0)
    stock = Column(Integer, nullable=False, default=0)
    sku = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    extra_attributes = Column(JSONB, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

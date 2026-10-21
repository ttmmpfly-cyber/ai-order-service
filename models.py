from datetime import datetime,timezone
from sqlalchemy import Boolean,DateTime,Float,ForeignKey,Integer,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from database import Base

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int]= mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    order_id:Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    customer_name:Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    product_name:Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    amount:Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status:Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    paid:Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at:Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )

    refunds:Mapped[list["Refund"]] = relationship(
        back_populates="order"
    )

class Refund(Base):
    __tablename__ = "refunds"

    id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    order_id:Mapped[str] = mapped_column(
        ForeignKey("orders.order_id"),
        nullable=False
    )

    reason:Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    status:Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False
    )

    created_at:Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )

    order:Mapped["Order"] = relationship(
        back_populates="refunds"
    )

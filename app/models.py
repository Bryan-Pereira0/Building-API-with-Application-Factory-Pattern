from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import date 
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)


service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    db.Column("ticket_id", ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", ForeignKey("mechanics.id"))
)

class Customers(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150),unique=True)
    phone: Mapped[int] = mapped_column(db.Integer, nullable=False)
    
    service_tickets: Mapped[List["ServiceTickets"]] = db.relationship(back_populates="customers")
    
class Mechanics(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True)
    phone: Mapped[int] = mapped_column(db.Integer, nullable=False)
    salary: Mapped[int] = mapped_column(db.Integer)
    
    service_mechanics: Mapped[List["Mechanics"]] = db.relationship(secondary="service_mechanics")
    

class ServiceTickets(Base):
    __tablename__ = "service_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))
    
    customers: Mapped["Customers"] = db.relationship(back_populates="service_tickets")
    service_mechanics: Mapped[List["ServiceTickets"]] = db.relationship(secondary="service_mechanics")

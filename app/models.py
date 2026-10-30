from flask_login import UserMixin
from typing import Optional
from decimal import Decimal
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), unique=True, index=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(
        sa.String(256), nullable=False)


# Product has an id, name, description, image file path, and relates to ProductStore.
class Product(db.Model):
    __tablename__ = "products"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(
        sa.String(150), index=True, nullable=False)
    description: so.Mapped[str | None] = so.mapped_column(sa.Text)
    img_ref: so.Mapped[str | None] = so.mapped_column(sa.String(500))
    category: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)

    stores: so.Mapped[list["ProductStore"]] = so.relationship(
        back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product {self.name}>"


# Store information, shared by multiple product listings.
class Store(db.Model):
    __tablename__ = "stores"
    __table_args__ = (sa.UniqueConstraint(
        "name", "location", name="uq_store_name_location"),)

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(
        sa.String(150), index=True, nullable=False)
    location: so.Mapped[str | None] = so.mapped_column(
        sa.String(255), nullable=False)

    product_listings: so.Mapped[list["ProductStore"]
                                ] = so.relationship(back_populates="store")

    def __repr__(self):
        return f"<Store {self.name} - {self.location}>"

# Connects a product to a store and stores its current price.


class ProductStore(db.Model):
    __tablename__ = "product_stores"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    product_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("products.id"), index=True, nullable=False)
    store_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("stores.id"), index=True, nullable=False)
    price: so.Mapped[Decimal] = so.mapped_column(
        sa.Numeric(10, 2), nullable=False)

    product: so.Mapped["Product"] = so.relationship(back_populates="stores")
    store: so.Mapped["Store"] = so.relationship(
        back_populates="product_listings")

    price_history: so.Mapped[list["PriceHistory"]] = so.relationship(
        back_populates="product_store",
        cascade="all, delete-orphan",
        order_by="PriceHistory.recorded_at")

    def __repr__(self):
        return f"<ProductStore {self.store.name} - {self.price}>"


# Stores historical prices for each product-store listing.
class PriceHistory(db.Model):
    __tablename__ = "price_history"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int | None] = so.mapped_column(sa.ForeignKey("users.id"), index=True, nullable=True)

    product_store_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("product_stores.id"), index=True, nullable=False)
    price: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(10, 2), nullable=False)
    recorded_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False
    )

    product_store: so.Mapped["ProductStore"] = so.relationship(back_populates="price_history")

    def __repr__(self):
        return f"<PriceHistory {self.price} - {self.recorded_at}>"

@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
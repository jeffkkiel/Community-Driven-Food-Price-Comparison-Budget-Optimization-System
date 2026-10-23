from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from app import db



#Product has an id, name, description, image file path, and relates to product_store table
class Product(db.Model):
    __tablename__ = "products"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(150), index=True)
    description: so.Mapped[str | None] = so.mapped_column(sa.Text)
    img_ref: so.Mapped[str | None] = so.mapped_column(sa.String(500))

    #so.Mapped alone is not a column
    stores: so.Mapped[list["ProductStore"]] = so.relationship(
        back_populates="product",
        cascade="all, delete-orphan")

    def __repr__(self):
            return '<Product {}>'.format(self.name)

#Product has an id, product id, name, price, and relates to product and price_history table
class ProductStore(db.Model):
    __tablename__ = "product_stores"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("products.id"), index=True)
    store_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    price: so.Mapped[int] = so.mapped_column(sa.Integer)

    product: so.Mapped["Product"] = so.relationship(back_populates="stores")
    price_history: so.Mapped[list["PriceHistory"]] = so.relationship(
        back_populates="product_store",
        cascade="all, delete-orphan",
        order_by="PriceHistory.recorded_at")
    
    def __repr__(self):
        return '<ProductStore {} - {}>'.format(self.store_name, self.price)

#Product has an id, product id, name, price, date, and relates to product_store table
class PriceHistory(db.Model):
    __tablename__ = "price_history"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    product_store_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("product_stores.id"), index=True)
    price: so.Mapped[int] = so.mapped_column(sa.Integer)
    recorded_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True)

    product_store: so.Mapped["ProductStore"] = so.relationship(back_populates="price_history")

    def __repr__(self):
        return '<PriceHistory {} - {}>'.format(self.price, self.recorded_at)

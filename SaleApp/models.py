import json
from SaleApp import app, db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)



class Category(Base):
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref="category", lazy=True)

    def __str__(self):
        return self.name


class Product(Base):
    name = Column(String(100), nullable=False)
    image = Column(String(300), default="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")
    price = Column(Float, default=0)
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=False)


if __name__ =="__main__":
    with app.app_context():
        db.create_all()
        # c1 = Category(name="Mobile")
        # c2 = Category(name="Tablet")
        # c3 = Category(name="Laptop")
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        with open("data/products.json", encoding='utf-8') as f:
            products = json.load(f)
            for p in products:
                prod = Product(**p)
                db.session.add(prod)

            db.session.commit()
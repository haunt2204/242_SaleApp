import hashlib
import json
from SaleApp import db, app
from models import Category, Product, User


def load_categories():
    # with open("data/category.json", encoding='utf-8') as f:
    #     return json.load(f)
    return Category.query.all()

def add_user(name, username, password, avatar):
    u = User(name=name, username=username, password=str(hashlib.md5(password.encode('utf-8')).hexdigest()), avatar=avatar)
    db.session.add(u)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def count_product():
    return Product.query.count()

def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()

def load_products(q=None, cate_id=None, page=None):
    # with open("data/products.json", encoding='utf-8') as f:
    #     products = json.load(f)
    #     if q:
    #         products = [p for p in products if p['name'].find(q)>=0]
    #     if cate_id:
    #         products = [p for p in products if p['cate_id'].__eq__(int(cate_id))]
    #
    #     return products
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))
    if cate_id:
        query = query.filter(Product.cate_id.__eq__(cate_id))

    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page)-1)*size
        query = query.slice(start, start+size)

    return query.all()

def get_product_by_id(id):
    # with open("data/products.json", encoding='utf-8') as f:
    #     products = json.load(f)
    #     for p in products:
    #         if p["id"].__eq__(id):
    #             return p
    return Product.query.get(id)

if __name__=="__main__":
    print(load_products())
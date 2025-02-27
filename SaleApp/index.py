from flask import render_template, request
import dao
from SaleApp import app


@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    products = dao.load_products(q=q, cate_id=cate_id)
    return render_template("index.html", products=products)

@app.route('/products/<int:id>')
def details(id):
    prod = dao.get_product_by_id(id)

    return render_template('product-details.html', prod=prod)

@app.context_processor
def common_attributes():
    return {
        "cates": dao.load_categories()
    }

@app.route('/login')
def login_my_user():

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
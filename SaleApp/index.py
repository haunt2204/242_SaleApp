from flask import Flask, render_template, request
import dao

app = Flask(__name__)

@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    cates = dao.load_categories()
    products = dao.load_products(q=q, cate_id=cate_id)
    return render_template("index.html", cates=cates, products=products)

@app.route('/products/<int:id>')
def details(id):
    prod = dao.get_product_by_id(id)
    return render_template('product-details.html', prod=prod)

if __name__ == "__main__":
    app.run(debug=True)
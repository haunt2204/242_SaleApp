import math

from flask import render_template, request, redirect
import dao
from SaleApp import app, login, admin
from flask_login import login_user, current_user, logout_user
import cloudinary.uploader


@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    page = request.args.get("page")
    products = dao.load_products(q=q, cate_id=cate_id, page=page)
    return render_template("index.html", products=products, pages=int(math.ceil(dao.count_product()/app.config["PAGE_SIZE"])))

@app.route('/products/<int:id>')
def details(id):
    prod = dao.get_product_by_id(id)

    return render_template('product-details.html', prod=prod)

@app.context_processor
def common_attributes():
    return {
        "cates": dao.load_categories()
    }

@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect('/')

    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "Tài khoản hoặc mật khẩu không khớp!"

    return render_template('login.html', err_msg=err_msg)

@app.route('/login-admin', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)
    else:
        err_msg = "Tài khoản hoặc mật khẩu không khớp!"
    return redirect('/admin')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.route("/register", methods=['GET','POST'])
def register():
    err_msg = None
    if request.method.__eq__("POST"):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            name = request.form.get('name')
            username = request.form.get('username')
            avatar = request.files.get('avatar')
            path = None
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                path = res['secure_url']
            dao.add_user(name, username, password, path)
            return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp!"
    return render_template('register.html', err_msg=err_msg)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
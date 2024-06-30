from flask import render_template, redirect, flash, session
from forms import RegisterForm, LoginForm, EditUserForm, UploadProductForm, CommentsForm
from models import Product, User, Comments
from ext import app, db
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    return render_template("index.html",products = Product.query.all())


@app.route("/register", methods=["GET", "POST"])
def register():
    session.pop('_flashes', None)
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
        else:
            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered!', 'success')
    print(form.errors)
    return render_template("register.html", form=form)

@app.route("/registered_users")
@login_required
def users():
    registered_users = User.query.all()
    if current_user.role != "Admin":
        return redirect("/")

    return render_template("users.html", registered_users=registered_users)


@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = EditUserForm(username=user.username, password=user.password)
    if form.validate_on_submit():
        user.username = form.username.data
        user.password = form.password.data

        db.session.commit()
        if current_user.role != "Admin":
            return render_template("index.html")
        else:
            return redirect("/registered_users")
    return render_template("edit_user.html", form=form)





@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/registered_users")
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
    return render_template("login.html", form=form)


@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def prod(product_id):
    form = CommentsForm()
    product = Product.query.get(product_id)
    if form.validate_on_submit():
        commenter = current_user.username
        new_comment = Comments(commenter=current_user.username, text=form.comment.data, product_id=product.id)
        db.session.add(new_comment)
        db.session.commit()
    comments = Comments.query.filter_by(product_id=product_id).all()
    return render_template("products.html", product=product, form=form, comment=comments)


@app.route("/add_products", methods=["GET", "POST"])
@login_required
def product():

    form = UploadProductForm()
    if form.validate_on_submit():
        user_nick = current_user.username
        new_product = Product(user_nick=current_user.username, name=form.name.data, price=form.price.data)
        if form.image.data:
            image = form.image.data
            image.save(f"{app.root_path}\static\{image.filename}")
            new_product.image = image.filename
        db.session.add(new_product)
        db.session.commit()
        return redirect("/")
    return render_template("add_products.html", form=form)


@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/")

@app.route("/delete_comment/<int:comment_id>")
def delete_comment(comment_id):
    comments = Comments.query.get(comment_id)

    db.session.delete(comments)
    db.session.commit()

    return redirect(f"/products/{comments.product_id}")
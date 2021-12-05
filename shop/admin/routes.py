

import re
import os
from flask import redirect, render_template, url_for, flash, request, session
from werkzeug.utils import secure_filename
from shop import db, app, photos, bcrypt
#from .forms import addproducts

from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User
from shop.products.models import add_product, Brand, Category, add_img, add_product
import os




@app.route('/adminregister', methods=['GET', 'POST'] )
def register():
    form = RegistrationForm(request.form)
    
    if request.method == 'POST':# and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        #flash(f'Welcome {form.username.data}, thanks you for registering', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html',form=form, title='Registration Page')


@app.route('/admin', methods=['GET', 'POST'] )
def admin():
    # on veux etre obliger de se logger pour atteindre cette page
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    flash('you are logged', 'success')
    products = add_product.query.all()

    return render_template('admin/admin.html', title='admin page', products=products)


@app.route('/adminlogin', methods=['GET', 'POST'] )
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        print(form.username.data)
        print(form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Welcome {form.username.data}, you are now logged', 'succes')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('wrong password, do it again')
    return render_template('admin/login.html', form=form, title='login page')


@app.route('/categories')
def category():
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    category = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/category.html', title='category page', category=category )




@app.route('/brands')
def brands():
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='brand page', brands=brands )



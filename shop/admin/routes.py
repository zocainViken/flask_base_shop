

import re
import os
from flask import redirect, render_template, url_for, flash, request, session
from werkzeug.utils import secure_filename
from shop import db, app, photos, bcrypt
#from .forms import addproducts

from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User
from shop.customers.models import OrderWaitingToBeSent
from shop.products.models import add_product, Brand, Category, add_img, add_product
import os
import math

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

def tax_calculator(tax, price):
    # calculate %
    # (2.9*150/100)
    #  ==>
    # tax x price / 100
    money = float(price)
    taxing = float(tax)# 2.9%
    tax_amount = taxing * money / 100
    total = money + tax_amount
    return tax_amount, total




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

@app.route('/sells', methods=['POST','GET'])
def sells():
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    if request.method == 'GET':
        orders = OrderWaitingToBeSent.query.order_by(OrderWaitingToBeSent.id.desc()).all()
        return render_template('admin/orders.html', title='Sells page', orders=orders )
        
    elif request.method == 'POST':
        form = request.form
        container = list(form.listvalues())
        invoice = container[0][0]
        status = container[0][1]
        invoice_id = container[0][2]
        orders = OrderWaitingToBeSent.query.filter_by(id=invoice_id).first()
        if status == 'Pending':
            orders.status = 'Prepare'
        elif status == 'Prepare':
            orders.status = 'Shipping'
        elif status == 'Shipping':
            orders.status = 'Arrived'
        else:
            print('something went wrong with the status update')
            orders.status = orders.status
        db.session.commit()
        return redirect(url_for('sells'))

    else:
        print('something went wrong with the user interface')

@app.route('/incomes', methods=['POST','GET'])
def incomes(): 
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    if request.method == 'GET':
        print('GET Methods')
        orders = OrderWaitingToBeSent.query.order_by(OrderWaitingToBeSent.id.desc()).all()
        price = truncate(float(orders[0].amount), 2)
        paypal_fee = 2.9# %
        transaction_price = 0.33# cts
        #paypal ==> 5.22 + 0.33 = 5.55
        paypal_amount, _ = tax_calculator(float(paypal_fee), price)
        paypal_amount = float(paypal_amount) + float(transaction_price)
        paypal_amount = truncate(paypal_amount, 2)

        tva = truncate(float(orders[0].tva), 2)

        for_me = price - paypal_amount - tva
        total_for_me = len(orders) * for_me

        total_tva = len(orders) * tva
        total_paypal = len(orders) * paypal_amount

        total = len(orders) * price
        return render_template('admin/income.html', title='Incomes page', amounts=orders,
                                paypal_amount=paypal_amount, for_me=for_me, total_for_me=total_for_me,
                                total_tva=total_tva, total_paypal=total_paypal, total=total)

    elif request.method == 'POST':
        print('POST Methods')

@app.route('/validate_order', methods=['POST','GET'])
def validate_order():
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    print(request.get_data())
    return 'need to change pending status to prepare and shipping'













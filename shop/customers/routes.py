



from operator import ipow
from flask import redirect, render_template, url_for, flash, request, session, request, make_response

from shop import db, app, photos, bcrypt, search, login_manager
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerLoginForm, CustomerRegestrationForm
from .models import Register, CustomerOrder
import os
import secrets
from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User
import pdfkit
from flask_wtf import FlaskForm






@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('mono_product'))
        else:
            flash('Incorrect credential', 'danger')
            return redirect(url_for('customerLogin'))
    return render_template('customer/logincustomer.html', form=form)


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegestrationForm()
    if form.validate_on_submit():
        next = request.args.get('next')
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(
                            name=form.name.data, username=form.username.data, email=form.email.data,
                            password=hash_password, country=form.country.data, state=form.state.data,
                            city=form.city.data, adress=form.adress.data, zipcode=form.zipcode.data
                            )
        db.session.add(register)
        db.session.commit()
        flash(f'thanks {form.name.data} for you\'re registration', 'success')
        #return url_for('customerLogin', form=form)
        return redirect(next or url_for('customerLogin', form=form))
    return render_template('customer/register.html', form=form)



@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customerLogin'))


@app.route('/customer/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = session['_user_id']
        #print(session)
        invoice = secrets.token_hex(5)

    try:
        order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
        db.session.add(order)
        db.session.commit()
        session.pop('Shoppingcart')
        flash('You\'re order has been sent', 'success')
        return redirect(url_for('orders', invoice=invoice))

    
    except Exception as e:
        print(str(e))
        flash('something went wrong with the order', 'danger')
        return redirect(url_for('getCart'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = session['_user_id']
        print(session)
        customer = Register.query.filter_by(id=customer_id).first()
        print(customer)
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).first()
        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100) * float(product['price'])
            subTotal =  float(product['price']) * int(product['quantity'])

            subTotal -= discount
            tax = ('%.2f' % (.06 * float(subTotal)))
            grandTotal = float('%.2f' % (1.06 * subTotal))
        
    else:
        return redirect(url_for('customerLogin'))

    return render_template('customer/order.html', invoice=invoice, tax=tax, subTotal=subTotal,
                            grandTotal=grandTotal, customer=customer, orders=orders)




@app.route('/get_pdf/<invoice>')
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = session['_user_id']
        if request.method == 'GET':
            print('posted data for pdf')
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).first()
            for _key, product in orders.orders.items():
                discount = (product['discount'] / 100) * float(product['price'])
                subTotal =  float(product['price']) * int(product['quantity'])

                subTotal -= discount
                tax = ('%.2f' % (.06 * float(subTotal)))
                grandTotal = float('%.2f' % (1.06 * subTotal))


        rendered = render_template('customer/pdf.html', invoice=invoice, tax=tax, subTotal=subTotal,
                                grandTotal=grandTotal, customer=customer, orders=orders)

        path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        options = {'enable-local-file-access': None}
        pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
        response = make_response(pdf)
        response.headers['content-Type'] = 'application/pdf'
        response.headers['content-Disposition'] = 'inline: filename='+invoice+'.pdf'
        return response
    
    return redirect(url_for('orders'))



'''
@app.route('/customer/login', methods=['GET', 'POST'] )
def customerlogin():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Welcome {form.username.data}, you are now logged', 'succes')
            return redirect(request.args.get('next') or url_for('getCart'))
        else:
            flash('wrong password, do it again')
    return render_template('customer/logincustomer.html', form=form, title='login page')

'''



















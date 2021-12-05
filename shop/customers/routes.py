
from operator import ipow
from flask import redirect, render_template, url_for, flash, request, session, request, make_response

from shop import db, app, photos, bcrypt, search, login_manager
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerLoginForm, CustomerRegestrationForm, UncustomerRegestrationForm
from .models import Register, CustomerOrder, OrderProcessing, OrderWaitingToBeSent
import os
import secrets
from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User
from shop.products.models import  Color, add_product
import pdfkit
from flask_wtf import FlaskForm


#https://kodify.net/python/math/truncate-decimals/
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

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = UncustomerRegestrationForm()# Make a New db for the customer witout loggin and made a class for it
    if form.validate_on_submit():
        next = request.args.get('next')
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(
                            name=form.name.data, username=form.username.data, email=form.email.data,
                            country=form.country.data, state=form.state.data, city=form.city.data, 
                            adress=form.adress.data, zipcode=form.zipcode.data
                            )
        db.session.add(register)
        db.session.commit()
        flash(f'thanks {form.name.data} for you\'re registration', 'success')
        #return url_for('customerLogin', form=form)
        return redirect(next or url_for('customerLogin', form=form))
    return render_template('customer/checkout.html', form=form)
    # basic form checkout for people that are not logged
    # what i need : name, first name , adress, some data payment
    return render_template('customer/checkout.html')

@app.route('/customer/interface', methods=['GET', 'POST'])
def user_interface():
    if current_user.is_authenticated:
        if request.method == 'GET':
            print('GET METHOD')
        
        elif request.method == 'POST':
            print('POST METHOD')

        else:
            print('something went wrong with the user interface')


        return render_template('customer/interface.html')
    else:
        print('You are not suposed to be here')
    return redirect(url_for('customerLogin'))









@app.route('/customer/interface/<invoice>', methods=['GET', 'POST'])
def last_order(invoice):
    if current_user.is_authenticated:
        if request.method == 'GET':
            print('put on user eyes a resume order and the possiblity of getting a pdf of it')
            # I need to connect to the last order with invoice id
            last_order = OrderWaitingToBeSent.query.filter_by(invoice=invoice).first()
            print(last_order)
            product_name = last_order.product_name
            print(product_name)
            product_image = add_product.query.filter_by(name=product_name).first()
            print(product_image)
            product_image = product_image.image_1
            # select from where invoice = invoice
            # put in on screen

            price = truncate(float(last_order.amount), 2)
            tva = truncate(float(last_order.tva), 2)
            return render_template('customer/last_order.html',
                                    invoice=invoice, order=last_order,
                                    product_image=product_image, price=price, tva=tva)
        
        elif request.method == 'POST':
            # probably for getting a pdf
            last_order = OrderWaitingToBeSent.query.filter_by(invoice=invoice).first()
            product_name = last_order.product_name
            product_image = add_product.query.filter_by(name=product_name).first()
            product_image = product_image.image_1
            price = truncate(float(last_order.amount), 2)
            tva = truncate(float(last_order.tva), 2)
            rendered = render_template('customer/pdf_template.html',
                                    invoice=invoice, order=last_order,
                                    product_image=product_image, price=price)
            
            print('data posted for pdf')
            #path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
            #config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            css=['shop/static/css/pdf.css']
            options = {'enable-local-file-access': None}
            #pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
            pdf = pdfkit.from_string(rendered, False, options=options, css=css)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'inline: filename='+invoice+'.pdf'
            return response

        else:
            print('something went wrong with the shipping address process')


        return render_template('customer/interface.html')
    else:
        print('You are not suposed to be here')
    return redirect(url_for('customerLogin'))











@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    print(form.password.data)
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
                            city=form.city.data, address=form.adress.data, zipcode=form.zipcode.data
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
        invoice = secrets.token_hex(5)

    try:
        order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
        db.session.add(order)
        db.session.commit()
        session.pop('Shoppingcart')
        #return redirect(url_for('orders', invoice=invoice))
        return redirect(url_for('comfirm_order', invoice=invoice))

    
    except Exception as e:
        print(str(e))
        flash('something went wrong with the order', 'danger')
        return redirect(url_for('getCart'))

@app.route('/comfirm_order/<invoice>', methods=['GET', 'POST'])
def comfirm_order(invoice):
    if current_user.is_authenticated:
        customer_id = session['_user_id']
        # here I need to:
        # get customer address
        # get paypal shipping address
        # ==>
        # compare them and pre-fill form for validation order
        if request.method == 'GET':
            # get customer address
            customer = Register.query.filter_by(id=customer_id).first()
            # I will use this email to comfirm customer
            #customer_mail = customer.email
            #customer_country = customer.country#france
            #customer_state = customer.state#bretagne


            # get paypal shipping address
            payer = OrderProcessing.query.filter_by(payer_email=customer.email).first()
            '''print(type(payer))
            payer_country = payer.country_code#FR
            payer_city = payer.city_1#brest
            payer_address = payer.street#13 routes des enfers
            payer_zipcode = payer.postal_code#29400'''

            # price ht, price + tva
            unit_amount = payer.unit_amount
            #payer_zipcode = payer.zipcode
            # ==>
            # compare them and pre-fill form for validation order

            # get order information
            orders = CustomerOrder.query.filter_by(customer_id=customer_id)[-1]# The Last Order
            invoice = orders.invoice
            for _key, product in orders.orders.items():
                print(f'\nProduct:\n{product}\n\n')
                product_color = product['color']
                product_name = product['name']
                product_image = product['image']

                discount = (product['discount'] / 100) * float(product['price'])
                sub_total =  float(product['price']) * int(product['quantity'])

                sub_total -= discount
                sub_total = float(product['price']) * int(product['quantity'])
                tax, grand_total = tax_calculator(20, sub_total)

            
            return render_template('customer/comfirm_order.html',
                                    invoice=invoice,tax=tax, subTotal=sub_total,
                                    grand_total=grand_total, customer=customer,
                                    orders=orders, product_color=product_color,
                                    product_name=product_name, payer=payer,
                                    product_image=product_image)

            
        elif request.method == 'POST':
            ''' if everythings is ok we can get the form data
                for stock them into database while the order is on 
                working'''
            form = request.form
            # https://www.reddit.com/r/flask/comments/hundt0/better_way_to_convert_immutablemultidict_to_list/)
            container = list(form.listvalues())
            print(container)
            color       = container[0][0]
            customer_id = container[1][0]
            invoice     = container[2][0]
            payer_id    = container[3][0]
            tva_amount  = container[4][0]
            total       = container[5][0]
            firstname   = container[6][0]
            name        = container[7][0]
            mail        = container[8][0]
            phone       = container[9][0]
            country     = container[10][0]
            state       = container[11][0]
            city        = container[12][0]
            street      = container[13][0]
            postal_code = container[14][0]
            product_id  = container[15][0]

            # now i need to put all this tuff into db
            order = OrderWaitingToBeSent(customer_id=customer_id, invoice=invoice,
                                         payer_id=payer_id, color=color,
                                         firstname=firstname, name=name,
                                         mail=mail,phone=phone,
                                         country=country, state=state,
                                         city=city, street=street,
                                         postal_code=postal_code,
                                         amount=total, tva=tva_amount,
                                         product_name=product_id)
            db.session.add(order)
            db.session.commit()
            # and we don't forget to decrease product stock
            # from color get id
            color_id = Color.query.filter_by(name_color=color).first()
            color_id = int(color_id.id)
            # from product where id_color stock -= 1
            stock = add_product.query.filter_by(colors_id=color_id).first()
            amount = int(stock.stock)
            if amount >= 0:
                if amount == 3:
                    print(f'only {amount} items left before youd send all you\'r stuff sweetie')

                amount -= 1
                # replace stock into db by our new fresh stock value
                # Replacing data is respected.
                stock.stock = amount
                db.session.commit()
                print('stock correctly update')
                return redirect(url_for('last_order', invoice=invoice))
                
            else:
                print(' you have no stock darling ')
                print('you need to block the add cart function for this product')



            return  redirect(url_for('user_interface'))
        
        else:
            print('something went wrong with the shipping address process')
    else:
        return redirect(url_for('customerLogin'))
    
    return redirect(url_for('customerLogin'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = session['_user_id']
        customer = Register.query.filter_by(id=customer_id).first()
        print(customer)
        orders = CustomerOrder.query.filter_by(customer_id=customer_id)[-1]# The Last Order
        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100) * float(product['price'])
            subTotal =  float(product['price']) * int(product['quantity'])

            subTotal -= discount
            tax = ('%.2f' % (.06 * float(subTotal)))
            grandTotal = float('%.2f' % (1.06 * subTotal))

        # I need to work here
        # here I will work on comfirm shipping address from paypal data
        paypal_data = CustomerOrder.query.filter_by(customer_id=customer_id)[-1]# The Last Order
        
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



















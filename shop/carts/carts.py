

# not forgot to load in init root file else it will not work


from logging import exception
from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop  import db, app
from shop.products.models import add_product
from shop.routes import brands, categories


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

def drink(sentence):
    print(f'\n\n', sentence, '\n\n\n')

def dict_merger(dict_1, dict_2):
    if isinstance(dict_1, list) and isinstance(dict_2, list):
        return dict_1 + dict_2
    
    elif isinstance(dict_1, dict) and isinstance(dict_2, dict):
        return dict(list(dict_1.items()) + list(dict_2.items()))
    
    return False



@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = add_product.query.filter_by(id=product_id).first()

        if colors == None:
            colors = 'default'
        
        drink(quantity)
            
        if len(product_id) >= 1 and len(quantity) >= 1 and len(colors) >= 1:
            dict_item = {
                product_id:{
                    'name':product.name,
                    'price':int(product.price),
                    'discount':int(product.discount),
                    'image':product.image_1,
                    'quantity':quantity,
                    'color':product.color.name_color
                }
            }
            
            if 'Shoppingcart' in session:
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                            
                else:
                    session['Shoppingcart'] = dict_merger(session['Shoppingcart'], dict_item)
            else:
                drink('new session')
                session['Shoppingcart'] = dict_item
                return redirect(request.referrer)

    
    except Exception as e:
        print(str(e))
        print('carts.py line 71')

    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    if'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    subtotal = 0
    grandtotal = 0
    TVA = 20
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount'] / 100 ) * float(product['price'])
        subtotal += float(product['price'])# * int(product['quantity'])
        subtotal -= discount
        
        tax, grandtotal = tax_calculator(TVA, subtotal)

    return render_template('products/carts.html',title='cart page', tax=tax, grandtotal=grandtotal, brands=brands(), categories=categories())


@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(str(e))

@app.route('/clearcart')
def clearcart(): 
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    
    except Exception as e:
        drink(str(e))


# doesn't work
@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
       
        
        try:
            session.modified = True
            
            for item in session['Shoppingcart']:
                
                if int(item) == code:
                    drink(item)
                    item['quantity'] = int(quantity)
                    item['color'] = int(color) 
                    flash('Item is updated')
                    drink(item['color'])
                return redirect(url_for('getCart'))
        except Exception as e:
            print('erreur:  ', str(e))
            return redirect(url_for('getCart'))



@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
        return redirect(url_for('getCart'))
    except Exception as e:
        drink(str(e))
        return redirect(url_for('getCart'))














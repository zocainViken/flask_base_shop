
import re
import os
from shop.admin.routes import admin
from flask import redirect, render_template, url_for, flash, request, session
from werkzeug.utils import secure_filename
from shop import db, app, photos
from .models import Brand, Category, Color, add_img, add_product
from .forms import Addproducts
#from shop.products.models import addproducts

def drink(sentence):
    print(f'\n\n{sentence}:\t', sentence, '\n\n\n')



@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        get_brand = request.form.get('category')
        cat = Category(name=get_brand)
        db.session.add(cat)
        flash(f'the category {get_brand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addcat.html')

@app.route('/updatecats/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))
    
    #print(f'\n\nid:\t', id, '\n\n\n') 
    updatecat = Category.query.get_or_404(id)# models so sql request for getting id
    categories = request.form.get('category') 
    #print(f'\n\nfile:\t', categories, '\n\n\n') 
    if request.method == 'POST':
        updatecat.name = categories
        flash(f'your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('category'))

    return render_template('/products/updatebrands.html', title='update category page', updatecat=updatecat)

@app.route('/deletecat/<int:id>', methods=['POST', 'GET'])
def deletecategory(id):
    cat = Category.query.get_or_404(id)
    #drink('delete sent')
    db.session.delete(cat)
    db.session.commit()
    flash(f'the category name: {cat}, was successfully deleted', 'success')
    return redirect(url_for('category'))





@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        get_brand = request.form.get('brand')
        brand = Brand(name=get_brand)
        db.session.add(brand)
        flash(f'the brand {get_brand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html')

@app.route('/updatebrands/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))
    
    #print(f'\n\nid:\t', id, '\n\n\n') 
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand') 
    #print(f'\n\nfile:\t', brand, '\n\n\n') 
    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))

    return render_template('products/updatebrands.html', title='update brand page', updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['POST', 'GET'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    flash(f'the brand name: {brand}, was successfully deleted', 'success')
    return redirect(url_for('brands'))




ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/addproduct', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    # DB fetching for html selector
    brands = Brand.query.all()
    category = Category.query.all()
    colors = Color.query.all()
    form = Addproducts(request.form)
    images = []# nom des images que je veux associer
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config ['UPLOAD_FOLDER'], filename))
                images.append(file.filename)
                flash(f"file:\t{filename.lower()}")
                path = f'{os.getcwd()}\\static\\images\\{file.filename}'
                product_name = form.name.data
                #print(f'\n\nfile:\t', path, '\n\n\n')
                adding = add_img(name=file.filename, product_name=product_name, path= path)
                db.session.add(adding)
                db.session.commit()


        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = request.form.get('color_name')
        description = form.description.data

        brand = request.form.get('brand')
        category = request.form.get('category')
        #print(f'\n\nfile:\t', brand, '\n\n\n')
        # if file and allowed_file(file.filename): 
        try:
            image_1 = request.files.get('image_1')
            image_1_name = secure_filename(image_1.filename)
            image_1.save(os.path.join(app.config ['UPLOAD_FOLDER'], image_1_name))

            image_2 = request.files.get('image_2')
            image_2_name = secure_filename(image_2.filename)
            image_2.save(os.path.join(app.config ['UPLOAD_FOLDER'], image_2_name))

            image_3 = request.files.get('image_3')
            image_3_name = secure_filename(image_3.filename)
            image_3.save(os.path.join(app.config ['UPLOAD_FOLDER'], image_3_name))
        except FileNotFoundError:
            print("no picture into form")
            
            image_1_name, image_2_name, image_3_name = 'NaN'
            # that work but all or nothing
            
        #print(f'\n\nfile:\t', files.filename, '\n\n\n')
        adding = add_product(name=name, price=price, discount=discount,
                             stock=stock, colors_id=colors, description=description,
                             brand_id=brand, category_id=category, image_1=image_1_name,
                             image_2=image_2_name, image_3=image_3_name)
        db.session.add(adding)
        db.session.commit()
        flash(f'the product {name} was successfuly added to your database', 'success')
        
        return render_template('products/addproduct.html')

    return render_template('products/addproduct.html', title='add product page',brands=brands,categories=category, colors=colors)# form=form,  categories=category)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))
    
    #print(f'\n\nid:\t', id, '\n\n\n') 
    brands = Brand.query.all()
    categories = Category.query.all()
    colors = Color.query.all()
    
    updateproduct = add_product.query.get_or_404(id)
    form = Addproducts(request.form)

    name = request.form.get('name') 
    if request.method == 'POST':
        updateproduct.colors = request.form.get('color')
        print(request.form.get('color'))
        updateproduct.name = form.name.data
        updateproduct.price = request.form.get('price')
        updateproduct.dicsount = form.discount.data
        updateproduct.stock = form.stock.data

        updateproduct.image_1
        updateproduct.image_2
        updateproduct.image_3

        db.session.commit()
        flash(f'the product {name} was successfuly added to your database', 'success')
        return redirect(url_for('admin'))

    return render_template('products/updateproducts.html', title='update product page',
            updateproduct=updateproduct, brands=brands, categories=categories, colors=colors)


@app.route('/deleteproduct/<int:id>', methods=['POST', 'GET'])
def deleteproduct(id):
    product = add_product.query.get_or_404(id)
    #drink('delete sent')
    db.session.delete(product)
    db.session.commit()
    flash(f'the product name: {product}, was successfully deleted', 'success')
    return redirect(url_for('admin'))

@app.route('/addcolor', methods=['GET', 'POST'])
def add_color():
    if 'username' not in session:
        flash('please loggin first', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':    
        get_color = request.form.get('name_color')
        
        color = Color(name_color=get_color)
        print(request.form)
        db.session.add(color)
        db.session.commit()
        flash(f'the color {get_color} was successfuly added to your database', 'success')
        
        return render_template('products/add_colors.html')

    return render_template('products/add_colors.html', title='add color page')# form=form,  categories=category)

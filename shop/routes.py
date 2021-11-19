
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask.templating import render_template_string

from shop import app, db, bcrypt

from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User
from shop.products.models import Category, add_product, Brand
import os



def drink(sentence):
    print(f'\n\n{sentence}:\t', sentence, '\n\n\n')

def brands():
    brands = Brand.query.join(add_product, (Brand.id == add_product.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(add_product, (Category.id == add_product.category_id)).all()
    return categories





@app.route('/', methods=['GET', 'POST'] )
def home():
    page = request.args.get('page', 1, type=int)
    products = add_product.query.filter(add_product.stock > 0).paginate(page=page, per_page=5)
    #return render_template('products/index.html', title='home page', products=products, brands=brands(), categories=categories())
    return render_template('products/skull.html', title='home page')


@app.route('/monoproduct', methods = ['GET', 'POST'])
def mono_product():
    page = request.args.get('page', 1, type=int)
    products = add_product.query.filter(add_product.stock > 0).paginate(page=page, per_page=5)
    return render_template('products/monoproduct.html', title='product page', products=products)

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = add_product.query.msearch(searchword, fields=['name', 'description'], limit=6)
    return render_template('products/result.html', products=products, brands=brands(), categories=categories())














@app.route('/products/<int:id>')
def single_page(id):
    products = add_product.query.get_or_404(id)
    return render_template('products/single_page.html', products=products, brands=brands(), categories=categories())

@app.route('/brand/<int:id>', methods=['POST', 'GET'])
def getbrand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = add_product.query.filter_by(brand=get_b).order_by(add_product.id.desc()).paginate(page=page, per_page=5)
    return render_template('products/index.html', title='brand page',categories=categories(), brand=brand, get_b=get_b, brands=brands())

@app.route('/categories/<int:id>', methods=['POST', 'GET'])
def getcategory(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = add_product.query.filter_by(category=get_cat).paginate(page=page, per_page=5)
    return render_template('products/index.html', title='category page',get_cat_prod=get_cat_prod, categories=categories(), page=page, brands=brands(), get_cat=get_cat)









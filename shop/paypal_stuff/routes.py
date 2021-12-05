

from shop import db, app
from flask_login import current_user
from flask import request, redirect, url_for, session
from .models import shippingParser



@app.route('/smart_button_ipn', methods=['POST'])
def smartbuttonipn():
    # from here i receive a response from paypal after the payment was done
    # also I need to store this data into db 
    data = request.get_json()
    shippingParser(data, True).put_in_db()

    return(data)

    








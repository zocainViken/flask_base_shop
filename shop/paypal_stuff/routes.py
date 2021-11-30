
from shop.customers.models import SentdexPaypalPayment
from shop import db, app


'''VERIFY_URL_PROD = 'https://ipnpb.paypal.com/cgi-bin/webscr'
VERIFY_URL_DEV =  'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'

VERIFY_URL = VERIFY_URL_DEV'''


from flask import render_template, request
from .models import shippingParser



@app.route('/smart_button_ipn', methods=['POST', 'GET'])
def smartbuttonipn():
    # from here i receive a response from paypal after the payment was done
    # also I need to store this data into db 
    data = request.get_json()
    shippingParser(data).put_it_in_db(True)

    return(data)



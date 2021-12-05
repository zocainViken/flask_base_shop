


from shop import db
from shop.customers.models import OrderProcessing

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

def tax_reductor(tax, price):
    # https://www.capte-les-maths.com/pourcentage/les_pourcentages_p10.php

    ##       Coefficient Multiplicateur = 1 +  20   = 1,2
    ##                                        _____
    ##                                         100
    #____________________________________________________________
    coeff_x = 1 + (tax / 100)#1.2


    ##        Prix Initial = 180  = 150
    ##                      ______
    ##                        1,2
    #____________________________________________________________
    no_tax = price / coeff_x#  150
    tax_amount = price - no_tax  #30

    return tax_amount, no_tax

class shippingParser():
    def __init__(self, data, debug=False):
        self.data = data

        # data send by js origin from smartbutton page
        # here I will filter the dict reponse for put the important data into database

        self.order_id = data['id']
        # 5N575537KH865605U  ==> use it in url for more detail on paypal

        self.order_intent = data['intent']
        # CAPTURE

        self.order_status = data['status']
        # COMPLETED

        self.create_time = data['create_time']
        # 2021-11-28T04:06:42Z

        self.update_time = data['update_time']
        # 2021-11-28T04:07:13Z

        self.merchand_id = data['purchase_units'][0]['payee']['merchant_id']
        # E7VZ3S7TB4HUA

        self.unit_reference_id = data['purchase_units'][0]['reference_id']
        # default

        self.street = data['purchase_units'][0]['shipping']['address']['address_line_1']
        # Av. de la Pelouse

        self.city_1 = data['purchase_units'][0]['shipping']['address']['admin_area_2']
        # Paris

        self.city_2 = data['purchase_units'][0]['shipping']['address']['admin_area_1']
        # Alsace

        self.postal_code =data['purchase_units'][0]['shipping']['address']['postal_code']
        # 75002

        self.country_code = data['purchase_units'][0]['shipping']['address']['country_code']
        # FR
        self.full_name =data['purchase_units'][0]['shipping']['name']['full_name']
        # John Doe

        self.unit_currency_code = data['purchase_units'][0]['amount']['currency_code']
        # EUR

        self.unit_amount = data['purchase_units'][0]['amount']['value']
        # 35.00

        self.payer_first_name = data['payer']['name']['given_name']
        # John

        self.payer_name = data['payer']['name']['surname']
        # Doe

        self.payer_mail = data['payer']['email_address']
        # sb-s60z28668822@personal.example.com

        self.payer_id = data['payer']['payer_id']
        # HPG6DCCZLRKW8

        self.link = data['links'][0]['href']
        # https://api.sandbox.paypal.com/v2/checkout/orders/5N575537KH865605U

        self.rel = data['links'][0]['rel']
        # self

        self.method = data['links'][0]['method']
        # GET

        # calculate paypal fee
        # (2.9*150/100)  ==> (tax x price / 100) + transaction_price
        price = float(self.unit_amount)
        tax_paypal = 2.9# 2.9%
        paypal_transaction_price = 0.33# 0.33 --> EUR
        tva = 20
        self.tva_amount, _ = tax_reductor(tva, price)# 30
        tax_amount, _ = tax_calculator(tax_paypal, price)#  paypal

        self.for_paypal = tax_amount + paypal_transaction_price#to paypal 5.22 + 0.33 = 5.55
        self.for_me = price - self.tva_amount - self.for_paypal# 180 - 30 - 5.55 = 144.5

        if debug:
            print('\n\n\t\t DEBUG MODE:\n\n')
            print('\n\n\t\t', self.data, ':\n\n\n\n')
            # Customer data
            print(f'NAME:\t{self.payer_name}\t FIRSTNAME:\t{self.payer_first_name }')
            print(f'FULLNAME:\t{self.full_name}\t PAYER_ID:\t{self.payer_id }')
            print(f'MAIL:\t{self.payer_mail } ')
            # Order part
            print(f'\nORDER_ID:\t{self.order_id}\t ORDER_INTENT:\t{self.order_intent }')
            print(f'ORDER_STATUS:\t{self.order_status}\n CREATE_TIME:\t{self.create_time }')
            print(f'LAST_UPDATE:\t{self.update_time }')
            print(f'MERCHANT_ID:\t{self.merchand_id}')
            print(f'UNIT_CUR:\t{self.unit_currency_code }\t UNIT_AMOUNT:\t{self.unit_amount}')
            # Shipping part
            print(f'STREET:\t{self.street}\nCITY_1:\t{self.city_1 }\nCITY_2:\t{self.city_2}')
            print(f'POSTAL:\t{self.postal_code } \tCOUNTRY:\t{self.country_code }')

            print('LINK:\t', self.link)
            print('REL:\t', self.rel)
            print('METHOD:\t', self.method)

            print('TVA_AMOUNT:\t', self.tva_amount)
            print('4 PAYPAL:\t', self.for_paypal)
            print('4 ME:\t', self.for_me)

    def put_in_db(self):

        print('here the function for put my data into DB')
        processing = OrderProcessing(
            order_id=self.order_id, order_intent=self.order_intent,
            order_status=self.order_status,
            street=self.street, city_1=self.city_1, city_2=self.city_2,
            postal_code=self.postal_code, country_code=self.country_code,
            unit_reference_id=self.unit_reference_id, unit_currency_code=self.unit_currency_code,
            unit_amount=self.unit_amount, full_name=self.full_name,
            payer_first_name=self.payer_first_name,
            payer_name=self.payer_name, payer_email=self.payer_mail,
            payer_id=self.payer_id, merchand_id=self.merchand_id,
            links=self.link, rel=self.rel, method=self.method,
            tva_amount=self.tva_amount, for_paypal=self.for_paypal,
            for_me=self.for_me, create_time=self.create_time, update_time=self.update_time,
            )

        db.session.add(processing)
        db.session.commit()
        print('shippingParser: data correctly processed')

# Create the flask object
from flask import *

from flask import  Flask, render_template,session,flash,redirect,url_for

from pymysql.connections import Connection

app = Flask(__name__)  # __name__ means main

# This secret key encrypts yur user session for security reasons
app.secret_key = 'AG_66745_hhYuo!@'  # 16

# print(__name__)  You can use this to check if your name == main
# this is the body of your project

import pymysql

connection = pymysql.connect(host='localhost', user='root', password='',
                             database='shoes_db')


# This slash represents your main page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/activewear')
def activewear():
    # create your query
    sql = "SELECT * FROM products_tbl"
    # execute/run
    # create a cursor used to execute sql
    cursor = connection.cursor()
    # now use the cursor to execute your sql.
    cursor.execute(sql)
    # check how many rows were returned
    if cursor.rowcount == 0:
        return render_template("activewear.html", msg="No product found")
    else:
        rows = cursor.fetchall()
        return render_template("activewear.html", rows=rows)

@app.route('/shoes')
def shoes():
    # create your query
    sql = "SELECT * FROM products_tbl"
    # execute/run
    # create a cursor used to execute sql
    cursor = connection.cursor()
    # now use the cursor to execute your sql.
    cursor.execute(sql)
    # check how many rows were returned
    if cursor.rowcount == 0:
        return render_template("shoes.html", msg="No product found")
    else:
        rows = cursor.fetchall()
        return render_template("shoes.html", rows=rows)

# this route will display single shoe
# this route will need a product id
@app.route('/single/<product_id>')
def single(product_id):
    # create your query, provide a %s placeholder
    sql = "SELECT * FROM products_tbl WHERE product_id = %s"
    # execute/run your
    # create a cursor used to execute sql
    cursor = connection.cursor()
    # Now use the cursor to execute your sql
    # below you provide id to replace the %s
    cursor.execute(sql, (product_id))

    # check how many rows were returned
    if cursor.rowcount == 0:
        return render_template('single.html', msg = 'Product does not exist')
    else:
        row  = cursor.fetchone()  # NB: product id was unique, so fetch one
        return render_template('single.html', row = row)

# this is the login route
# below route accepts a GET or a POST
@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        # receive the posted email and password as varaibles
        email = request.form['email']
        password = request.form['password']
        # we now move to the database and confirm if above details exist
        sql = "SELECT * FROM customers where email = %s and password=%s"
        # create a cursor and execute above sql
        cursor = connection.cursor()
        # execute the sql, provide email and password to fit %s placeholders
        cursor.execute(sql, (email, password))
        # check if a match was found
        if cursor.rowcount ==0:
            return render_template('login.html', error = 'Wrong Credentials')
        elif cursor.rowcount ==1:
            # create a user to track who is logged in
            # attach user email to the session
            session['user'] = email
            return  redirect('/shoes')
        else:
            return render_template('login.html', error='Error Occured, Try Later')
    else:
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        password2 = request.form['password2']
        gender = request.form['gender']
        address = request.form['address']
        dob = request.form['dob']

        ### Validations
        import re
        if password != password2:
            return render_template('register.html', password='Passwords do not match')

        elif len(password) < 8:
            return render_template('register.html', password='Passwords must have at least 8 characters')

        elif not re.search("[a-z]", password):
            return render_template('register.html', password='Must have a small letter')

        elif not re.search("[A-Z]", password):
            return render_template('register.html', password='Must have a capital letter')

        elif not re.search("[0-9]", password):
            return render_template('register.html', password='Must have a number')

        elif not re.search("[_@$]", password):
            return render_template('register.html', password='Must have a small letter')

        elif len(phone) < 10:
            return render_template('register.html', phone='Must have be 10 or more numbers')

        else:
            sql = "insert into customers(firstname, surname, email, phone, password, gender,address, dob) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            try:
                cursor.execute(sql, (firstname, surname, email, phone, password, gender, address, dob))
                connection.commit()
                return render_template('register.html', success='Registration Successful')
            except:
                return render_template('register.html', success='Registration Failed')

    else:
        return render_template('register.html')

@app.route('/reviews', methods=['POST', 'GET'])
def reviews():
    if request.method == 'POST':
        user = request.form['user']
        product_id = request.form['product_id']
        message = request.form['message']
        # Do a table for reviews
        sql = "insert reviews (user,product_id,message) values (%s,%s,%s)"
        cursor = connection.cursor()
        try:
            cursor.execute(sql, (user, product_id, message))
            connection.commit()

            ##Flash a message to show whether the review posting was a success or not
            flash('Review posted successfully')
            flash('Thank you for your review')
            return redirect(url_for('single', product_id=product_id))
        except:
            flash('Review not posted')
            flash('Please try again')
            return redirect(url_for('single', product_id=product_id))
    else:
        return ''

@app.route('/logout')
def logout():
    session.pop('user')  # clear session
    return redirect('/login')

@app.route('/account')
def account():
    return render_template('login.html')


# git link: https://github.com/modcomlearning/FlaskProject
# create a github.com account
# get below code here   https://github.com/modcomlearning/mpesa_sample
# create a payment.html   template
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth


@app.route('/mpesa_payment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # capture the session of paying client
        email = session['user']
        qtty = str(request.form['qtty'])
        product_id = str(request.form['product_id'])
        # multiply qtty * amount
        total_pay = float(qtty) * float(amount)

        # sql to insert data
        # create a table,payment_info
        sql = 'INSERT INTO `payment_info`( phone, email, qtty, total_pay, product_id) VALUES (%s,%s,%s,%s,%s)'
        cursor = connection.cursor()
        cursor.execute(sql, (phone, email, qtty, total_pay, product_id))
        connection.commit()

        # GENERATING THE ACCESS TOKEN
        consumer_key = "ma2e4xJqLXbgal5fx59KInEtMAY8tkYL"
        consumer_secret = "ai6OLzTGmAo2GdJo"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": total_pay,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": email,
            "TransactionDesc": 'Qtty: ' + qtty + ' ID: ' + product_id
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)

        return render_template('payment.html', msg='Please Complete Payment in Your Phone')
    else:
        return render_template('payment.html')


@app.route('/admin', methods = ['POST','GET'])
def admin():
    if request.method == 'POST':
        # receive the posted email and password as variables
        email = request.form['email']
        password = request.form['password']
        # we now move to the database and confirm if above details exist
        sql = "SELECT * FROM admin where email = %s and password=%s"
        # create a cursor and execute above sql
        cursor = connection.cursor()
        # execute the sql, provide email and password to fit %s placeholders
        cursor.execute(sql, (email, password))
        # check if a match was found
        if cursor.rowcount ==0:
            return render_template('admin.html', error = 'Wrong Credentials')
        elif cursor.rowcount ==1:
            # create a user to track who is logged in
            # attach user email to the session
            session['admin'] = email
            return  redirect('/dashboard')
        else:
            return render_template('admin.html', error='Error Occured, Try Later')
    else:
        return render_template('admin.html')

@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        sql = "select * from customers ORDER by reg_date DESC"
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return render_template('dashboard.html', msg= "No customers")
        else:
            rows = cursor.fetchall()
            return render_template('dashboard.html', rows=rows)  # create this template
    else:
        return redirect('/admin')

@app.route('/adminlogout')
def adminlogout():
    session.pop('admin')  # clear session
    return redirect('/admin')

@app.route('/customer_del/<customer_id>')
def customer_del(customer_id):
    if 'admin' in session:
        sql = 'delete from customers where customer_id=%s'
        cursor = connection.cursor()
        cursor.execute(sql, customer_id)
        connection.commit()
        flash("Delete Successful")
        return render_template('/dashboard')
    else:
        return redirect('/admin')


# check
if __name__ == '__main__':
    app.run(debug=True)

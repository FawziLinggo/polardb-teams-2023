import json
import os
import socket
import sys
from datetime import datetime, timedelta

import psycopg2 as psycopg2
from flask import Flask, request
from flask_mail import Mail, Message
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

# Logging
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# basic auth flask app
auth = HTTPBasicAuth()
user_auth = os.environ.get('USER_AUTH')
if user_auth is None:
    sys.exit("USER_AUTH environment variable is not set")
pass_auth = os.environ.get('PASS_AUTH')
if pass_auth is None:
    sys.exit("PASS_AUTH environment variable is not set")

users = {
    user_auth: pass_auth
}


# Email config
email_sender = os.environ.get('EMAIL_SENDER')
if email_sender is None:
    sys.exit("EMAIL_SENDER environment variable is not set")
    
email_password = os.environ.get('EMAIL_PASSWORD')
if email_password is None:
    sys.exit("EMAIL_PASSWORD environment variable is not set")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = email_sender
app.config['MAIL_PASSWORD'] = email_password


# Get environment for database
url_db = os.environ.get('URL_DB')
if url_db is None:
    sys.exit("URL_DB environment variable is not set")

name_db = os.environ.get('NAME_DB')
if name_db is None:
    sys.exit("NAME_DB environment variable is not set")

user_db = os.environ.get('USER_DB')
if user_db is None:
    sys.exit("USER_DB environment variable is not set")

pass_db = os.environ.get('PASS_DB')
if pass_db is None:
    sys.exit("PASS_DB environment variable is not set")

port_db = os.environ.get('PORT_DB')
if port_db is None:
    sys.exit("PORT_DB environment variable is not set")

# Connect to postgres database
conn = psycopg2.connect(
    host=url_db,
    port=port_db,
    database=name_db,
    user=user_db,
    password=pass_db
)
mail = Mail(app)

# auth handler
@auth.verify_password
def verify_password(username, password):
    if username in users and password == users[username]:
        return username

def get_email_receiver(id_):
    cur = conn.cursor()
    cur.execute("""SELECT email FROM public."user" where id = '{}'""".format(id_))
    email_receiver = cur.fetchone()[0]
    cur.close()
    return email_receiver

def insert_token_subscriber(name, username_token, token, expire30days, topic, symbol):
    try:
        cur = conn.cursor()
        query = """INSERT INTO public."token_kafka_subscriber" (username, username_token, token, expire, topic_name, symbol) 
                    VALUES ('{}','{}', '{}', '{}', '{}','{}')""".format(name, username_token, token, expire30days, topic, symbol)
        cur.execute(query)
        cur.close()
        conn.commit()
        logging.info("Success insert token kafka subscriber to database with name {} symbol {}".format(name, symbol))
        return "Success insert token kafka subscriber to database with name {} symbol {}".format(name, symbol)
    except Exception as e:
        logging.error("failed insert token kafka subscriber to database with name {} symbol {}".format(name, symbol))
        return str(e)
@app.route("/send-email-order", methods=['GET'])
@auth.login_required
def send_email():
    try:
        data = request.get_json()
        id_ = data['id']
        email_receiver = get_email_receiver(id_)
        logging.info("process send email order to {}".format(email_receiver))

        stock = data['stock']
        amount = data['amount']
        status_trade = data['status_trade']
        name = email_receiver.split("@")[0]
        Title = "Trading System Order"

        try:
            HTMLFile = open("templates/notif-order.html", "r")
            HTMLFile = HTMLFile.read().format(name=name, stock=stock, amount=amount, status_trade=status_trade)
            msg = Message(Title, sender=email_sender, recipients=[email_receiver])
            msg.html = HTMLFile
            mail.send(msg)
            logging.info("Email order sent! to {}".format(email_receiver))
            return "Email sent!"
        except Exception as e:
            logging.error(str(e) + " to {}".format(email_receiver))
            return json.dumps({"error": str(e), "status": "error"})
    except Exception as e:
        logging.error(str(e))
        return json.dumps({"error": str(e), "status": "error"})

@app.route("/send-email-subscriber", methods=['GET'])
@auth.login_required
def send_email_subscriber():
    try:
        data = request.get_json()
        id_ = data['id']
        email_receiver = get_email_receiver(id_)
        logging.info("process send email subscriber to {}".format(email_receiver))

        stock = data['stock']
        name = email_receiver.split("@")[0]
        Title = "Subscribe Realtime Emiten {}".format(stock)

        # Create Token Kafka
        username_token ="Xes3%2BZ%"
        token = "eySFEfsssFiesa"
        expire30days = datetime.now() + timedelta(days=30)
        topic = "stock-{}".format(stock)

        try:
            HTMLFile = open("templates/notif-subcriber.html", "r")
            HTMLFile = HTMLFile.read().format(name=name, stock=stock, topic_name=topic, username=username_token,
                                              token=token, expire30days=expire30days)
            msg = Message(Title, sender=email_sender, recipients=[email_receiver])
            msg.html = HTMLFile
            mail.send(msg)
            logging.info("Email subscriber sent! to {}".format(email_receiver))

            # Insert token kafka subscriber to database
            status_insert_databases = insert_token_subscriber(name, username_token, token, str(expire30days), topic, stock)
            return json.dumps({"status": "success", "message": status_insert_databases})
        except Exception as e:
            logging.error(str(e) + " to {}".format(email_receiver))
            return json.dumps({"error": str(e), "status": "error"})
    except Exception as e:
        logging.error(str(e))
        return json.dumps({"error": str(e), "status": "error"})

def update_balance_investor(username, balance):
    tabel = "investors_net_balance"
    schema = "public"
    try:
        cur = conn.cursor()
        query = """UPDATE {}.{} SET balance = '{}' WHERE username = '{}'""".format(schema, tabel, balance, username)
        cur.execute(query)
        cur.close()
        conn.commit()
        logging.info("Success update balance investor to database with name {}".format(username))
        return "Success update balance investor to database with name {}".format(username)
    except Exception as e:
        logging.error("failed update balance investor to database with name {}".format(username))
        return str(e)
@app.route("/investors-net-balance", methods=['POST'])
@auth.login_required
def investors_net_balance():
    tabel = "investors_net_balance"
    schema = "public"
    data = request.get_json()
    id_ = data['id']

    # check status buy or sell
    if data['status_trade'] == "buy":
        balance = data['amount']
    else:
        balance = -data['amount']

    email_investor = get_email_receiver(id_)
    username = email_investor.split("@")[0]
    try:
        # Select one investor
        cur = conn.cursor()
        query = """SELECT * FROM {}.{} WHERE username = '{}'""".format(schema, tabel, username)
        cur.execute(query)
        data_investor = cur.fetchone()
        if data_investor is None:
            query = """INSERT INTO {}.{} (username, email, balance) VALUES ('{}', '{}', 0)"""\
                .format(schema, tabel, username, email_investor)
            cur.execute(query)
            conn.commit()
            cur.close()
            logging.info("Success insert investor to database with name {}".format(username))
            update_balance_investor(username, balance)
            logging.info("Success update balance investor to database with name {}".format(username))
            return "Success insert investor to database with name {}".format(username)
        else:
            # Update balance investor
            # data : [username, email, balance]
            balance = data_investor[2] + balance
            update_balance_investor(username, balance)
            logging.info("Success update balance investor to database with name {}".format(username))
            return "Success update balance investor to database with name {}".format(username)

    except Exception as e:
        logging.error(str(e))
        return json.dumps({"error": str(e), "status": "error"})


if __name__ == '__main__':
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print(IPAddr)
    logging.info("Starting Email Service at port 5000")
    app.run(port=80, host=IPAddr)

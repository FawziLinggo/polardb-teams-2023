# How this program works
1. This program is a simple program to send email to customer, for order and subscriber.
2. This program is using gmail smtp server to send email.
3. This program is using flask to create API.
4. This program is using python 3.10
5. This program is using postgresql database to query data user.
6. This program is using docker to run this program.

## API (Port 5000)
1. /send-email-order - GET -data {id, stock, amount, status_trade}
2. /send-email-subscriber - GET

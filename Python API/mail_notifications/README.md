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


## How to run this program
1. build image 
```bash
docker build -t stockswizard-polardb/mail-notifications:latest .
```
2. run container    
```bash
docker run -d -p 5000:5000 --name stockswizard-polardb-mail-notifications stockswizard-polardb/mail-notifications:latest -e EMAIL_SENDER="" -e EMAIL_PASSWORD="" -e URL_DB="" -e NAME_DB="" -e USER_DB="" -e PASS_DB="" -e PORT_DB=""
```

3. check container
```bash
docker ps
```
4. check logs
```bash
docker logs stockswizard-polardb-mail-notifications
```
5. stop container
```bash
docker stop stockswizard-polardb-mail-notifications
```
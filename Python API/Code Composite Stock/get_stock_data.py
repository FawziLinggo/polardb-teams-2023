import sys

import psycopg2
import yfinance as yf
from pandas_datareader import data as pdr
from jproperties import Properties

yf.pdr_override()
date_start = "2022-06-01"
date_end = "2022-12-31"

# Read config file
configs = Properties()
with open('../../All-Config/config.properties', 'rb') as config_file:
    configs.load(config_file)
url_db = configs.get("url_db").data
name_db = configs.get("name_db").data
user_db = configs.get("user_db").data
pass_db = configs.get("pass_db").data
port_db = configs.get("port_db").data

print("config loaded")
# Connect to postgres database
try:
    conn = psycopg2.connect(
        host=url_db,
        port=port_db,
        database=name_db,
        user=user_db,
        password=pass_db
    )
    cur = conn.cursor()
    print("Database connected")
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    sys.exit(1)

cur.execute("SELECT symbol FROM stock")
print("Query executed")

# get the records from the database
records = cur.fetchall()
for record in records:
    symbol = str(record[0])
    print(symbol)
    cur.execute("SELECT id FROM stock WHERE symbol = %s", (symbol,))
    stock_id = cur.fetchone()[0]
    print(stock_id)
    symbol = symbol + ".JK"
    tests = pdr.get_data_yahoo(symbol, start=date_start, end=date_end)
    for i in range(len(tests)):
        date = tests.index[i]
        open = tests['Open'][i]
        high = tests['High'][i]
        low = tests['Low'][i]
        close = tests['Close'][i]
        adj_close = tests['Adj Close'][i]
        volume = tests['Volume'][i]
        query = "INSERT INTO stock_price (stock_id, date, open, high, low, close, adj_close, volume) " \
                "VALUES ({}, '{}', {}, {}, {}, {}, {}, {})".format(stock_id, date, open, high, low,
                                                                   close, adj_close, volume)
        cur.execute(query)
        print("Inserting data for " + symbol + " at " + str(date))
        conn.commit()
        print("Data inserted + committed")

cur.close()
conn.close()

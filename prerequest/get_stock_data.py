import psycopg2
import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()
date_start = "2022-06-01"
date_end = "2022-12-31"

# Connect to postgres database
conn = psycopg2.connect(
    host="192.168.35.79",
    database="trading_app",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()
cur.execute("SELECT symbol FROM stock")

# get the records from the database
records = cur.fetchall()
for record in records:
    symbol = record[0]
    cur.execute("SELECT id FROM stock WHERE symbol = %s", (symbol,))
    stock_id = cur.fetchone()[0]
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
        conn.commit()

cur.close()
conn.close()

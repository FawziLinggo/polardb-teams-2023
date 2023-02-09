import psycopg2
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from jproperties import Properties
from pydantic import BaseModel
from typing import List

# change port to 8080
app = FastAPI()
tempaltes = Jinja2Templates(directory="templates")

# Read config file
configs = Properties()
with open('../All-Config/config.properties', 'rb') as config_file:
    configs.load(config_file)
url_db = configs.get("url_db").data
name_db = configs.get("name_db").data
user_db = configs.get("user_db").data
pass_db = configs.get("pass_db").data
port_db = configs.get("port_db").data

# Connect to postgres database
conn = psycopg2.connect(
    host=url_db,
    port=port_db,
    database=name_db,
    user=user_db,
    password=pass_db
)


@app.get("/")
def index(request: Request):
    stock_filter = request.query_params.get("filter", "")
    cur = conn.cursor()
    if stock_filter == "new_closing_low":
        query = "SELECT symbol, company, MIN(volume) as volume, MAX(date) FROM ( SELECT symbol, company, stock_price.stock_id, volume , stock_price.date FROM stock_price JOIN stock ON stock.id = stock_price.stock_id ) as subq GROUP BY symbol, company, stock_id ORDER BY volume;"
        cur.execute(query)
        rows = cur.fetchall()
        print(rows)
        rows = [dict(symbol=row[0], company=row[1], volume=row[2]) for row in rows]
    else:
        # cur.execute("""SELECT id, symbol, company FROM stock ORDER BY symbol""")
        cur.execute(
            """SELECT symbol, company, max(volume) as volume, MAX(date) FROM ( SELECT symbol, company, stock_price.stock_id, volume , stock_price.date FROM stock_price JOIN stock ON stock.id = stock_price.stock_id ) as subq GROUP BY symbol, company, stock_id ORDER BY symbol;""")
        rows = cur.fetchall()
        rows = [dict(symbol=row[0], company=row[1], volume=row[2]) for row in rows]
    # print(rows)

    return tempaltes.TemplateResponse("index.html", {"request": request, "stocks": rows})


@app.get("/stock/{symbol}")
def stocl_detail(request: Request, symbol):
    cur = conn.cursor()
    cur.execute("""SELECT id, symbol, company FROM stock WHERE symbol = %s""", (symbol,))
    row = cur.fetchone()
    row = dict(id=row[0], symbol=row[1], company=row[2])

    cur.execute(
        """SELECT date, open, high, low, close, adj_close, volume FROM stock_price WHERE stock_id = %s ORDER by date DESC""",
        (row['id'],))
    prices = cur.fetchall()
    prices = [dict(date=price[0], open=price[1], high=price[2], low=price[3], close=price[4], adj_close=price[5],
                   volume=price[6]) for price in prices]
    return tempaltes.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices})


@app.get("/stock/TRST/chart")
async def stock_chart():
    data = [
        [1612489600000, 10.0],
        [1612576000000, 11.0],
        [1612662400000, 12.0],
        [1612748800000, 13.0],
        [1612835200000, 14.0],
        [1612921600000, 15.0]
    ]
    return data


class TradingStatus(BaseModel):
    user: str
    emiten: List[str]
    status: str



@app.post("/trading-status/")
async def create_item(item: TradingStatus):
    return {"user": item.user, "emiten": item.emiten, "status": item.status}

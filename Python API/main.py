import asyncio
import logging

import psycopg2
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from jproperties import Properties
from pydantic import BaseModel, StrictStr
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from pykafka import KafkaClient

def get_kafka_client():
    return KafkaClient(hosts='172.18.46.121:9092')


# change port to 8080
app = FastAPI(title="test")
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
tempaltes = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return tempaltes.TemplateResponse("404.html", {"request": request})


@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    return tempaltes.TemplateResponse("500.html", {"request": request})


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
    cur.close()
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
    cur.close()
    return tempaltes.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices})





class TradingStatus(BaseModel):
    user: str
    emiten: str
    status: str
    amount: float


@app.post("/trading-status/")
async def create_item(item: TradingStatus):
    return {"user": item.user, "emiten": item.emiten, "status": item.status, "amount": item.amount}


class Users(BaseModel):
    id: str
    email: str
    password: str
    username: str


@app.post("/register")
async def register(item: Users):
    # insert to database
    cur = conn.cursor()
    try:
        query = """INSERT INTO public.user (id, email, password, username) VALUES ('{}','{}', '{}', '{}')""" \
            .format(item.id,
                    item.email,
                    item.password,
                    item.username)
        print(query)
        cur.execute(query)
        conn.commit()
        cur.close()
        return {"id": item.id, "email": item.email, "password": item.password, "username": item.username}
    except Exception as e:
        cur.execute("ROLLBACK")
        cur.close()
        return {"error": str(e), "status code": 400}


@app.get("/subscribe/{symbol}")
def subscribe(request: Request, symbol):
    return tempaltes.TemplateResponse("subscribe_stock.html", {"request": request, "symbol": symbol})


@app.get("/login")
def login(request: Request):
    return tempaltes.TemplateResponse("login.html", {"request": request})


@app.get("/signup")
def login(request: Request):
    return tempaltes.TemplateResponse("signup.html", {"request": request})

@app.get("/faq")
def login(request: Request):
    return tempaltes.TemplateResponse("faq.html", {"request": request})

@app.get("/aboutus")
def login(request: Request):
    return tempaltes.TemplateResponse("about.html", {"request": request})


@app.get("/leaderboard")
def login(request: Request):
    tabel = "investors_net_balance"
    schema = "public"
    name = "fawzilinggo"
    cur = conn.cursor()
    query = """SELECT username, balance FROM {}.{} WHERE username = '{}'""".format(schema, tabel, name)
    cur.execute(query)
    row = cur.fetchone()
    print(row)
    balance = row[1]
    name = row[0]
    cur.close()
    return tempaltes.TemplateResponse("leaderboard.html",
                                      {"request": request,
                                       "balance": balance,
                                       "name": name})

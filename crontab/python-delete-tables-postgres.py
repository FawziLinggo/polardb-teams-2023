from datetime import datetime

import psycopg2
from jproperties import Properties

# Read config file
configs = Properties()
with open('../All-Config/config.properties', 'rb') as config_file:
    configs.load(config_file)
url_db = configs.get("url_db").data
name_db = configs.get("name_db").data
user_db = configs.get("user_db").data
pass_db = configs.get("pass_db").data
port_db = configs.get("port_db").data

conn = psycopg2.connect(
    host=url_db,
    port=port_db,
    database=name_db,
    user=user_db,
    password=pass_db
)

tabel_name = 'trading_order_realtime'

cur = conn.cursor()
delete_query = "SELECT * FROM " + tabel_name + " WHERE created_at < %s"
def delete_data():
    current_time = datetime.now().time()
    if current_time.hour == 0 and current_time.minute == 0:
        cur.execute(delete_query, (datetime.now().date(),))
        conn.commit()

# tutup koneksi
cur.close()
conn.close()

# panggil fungsi delete_data()
delete_data()
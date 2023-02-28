import logging

from ksql import KSQLAPI

client = KSQLAPI('http://172.18.46.121:8088')
logging.basicConfig(level=logging.DEBUG)

# Execute a SELECT statement
table_name = 'EODTradingSystemOrderToDB'
results = client.ksql('SELECT * FROM {} emit changes;').format(table_name)

# Print the results
for row in results:
    print(row)

create table EODTradingSystemOrderToDB (rowkey varchar primary key, symbol varchar,
    open double,
    high double,
    low double,
    close double,
    time varchar)
    with
    (kafka_topic='TradingSystemOrderProduction', value_format='json');
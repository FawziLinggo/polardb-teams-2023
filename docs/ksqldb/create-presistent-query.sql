create stream UsingSchemaToDB WITH(VALUE_FORMAT='AVRO') AS SELECT * FROM TradingSystemOrderToDB;
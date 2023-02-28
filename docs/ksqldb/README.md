Run stream processing on your data with ksqlDB
=============================================
set 'auto.offset.reset'='earliest';
select * from USINGSCHEMATODB emit changes;
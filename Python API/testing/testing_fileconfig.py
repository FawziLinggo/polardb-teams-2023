from jproperties import Properties

configs = Properties()
with open('../../All-Config/config.properties', 'rb') as config_file:
    configs.load(config_file)

print(configs.get("url_db").data)
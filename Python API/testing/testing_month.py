from datetime import datetime
from dateutil.relativedelta import relativedelta


start_date = datetime(2023, 12, 1)
end_date = datetime(2023, 1, 31)
for i in range(0, 3):
    for j in range(0, 31):
        print(start_date + relativedelta(months=i, days=j))
from datetime import datetime, timedelta

start_date = datetime(2023, 3, 1)
end_date = datetime(2023, 12, 19)

date_list = []

while start_date <= end_date:
    yyyymmdd = start_date.strftime("%Y%m%d")
    date_list.append(yyyymmdd)
    start_date += timedelta(days=1)

new_list = []

for date_string in date_list:
    for hour in range(24):
        yyyymmddhh = date_string + str(hour).zfill(2)
        new_list.append(yyyymmddhh)

print(new_list)
print(len(new_list))
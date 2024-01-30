import pandas as pd

file_path = '2022-10.csv'
i = 93
for a in range(1):
    columns_to_read = list(range(0, 3)) + list(range(i, i + 45))

    df = pd.read_csv(file_path, usecols=columns_to_read, encoding='gbk')

    df.to_csv(f'weather_data/{i + 1}_{i + 45}.csv', index=False, header=False)
    i += 3

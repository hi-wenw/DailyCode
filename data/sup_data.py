import pandas as pd
import os

if __name__ == '__main__':
    file_list = os.listdir('weather_data')
    for file in file_list:
        df = pd.read_csv(f'weather_data/{file}', encoding='utf8',
                         names=['area', 'province', 'city',
                                'd_high_1', 'd_low_1', 'd_wea_1',
                                'd_high_2', 'd_low_2', 'd_wea_2',
                                'd_high_3', 'd_low_3', 'd_wea_3',
                                'd_high_4', 'd_low_4', 'd_wea_4',
                                'd_high_5', 'd_low_5', 'd_wea_5',
                                'd_high_6', 'd_low_6', 'd_wea_6',
                                'd_high_7', 'd_low_7', 'd_wea_7',
                                'd_high_8', 'd_low_8', 'd_wea_8',
                                'd_high_9', 'd_low_9', 'd_wea_9',
                                'd_high_10', 'd_low_10', 'd_wea_10',
                                'd_high_11', 'd_low_11', 'd_wea_11',
                                'd_high_12', 'd_low_12', 'd_wea_12',
                                'd_high_13', 'd_low_13', 'd_wea_13',
                                'd_high_14', 'd_low_14', 'd_wea_14',
                                'd_high_15', 'd_low_15', 'd_wea_15',
                                ])

        df = df.reindex(columns=['area', 'province', 'city',
                                 'd_high_1', 'd_low_1', 'd_high_2',
                                 'd_low_2', 'd_high_3', 'd_low_3',
                                 'd_high_4', 'd_low_4', 'd_high_5',
                                 'd_low_5', 'd_high_6', 'd_low_6',
                                 'd_high_7', 'd_low_7', 'd_high_8',
                                 'd_low_8', 'd_high_9', 'd_low_9',
                                 'd_high_10', 'd_low_10', 'd_high_11',
                                 'd_low_11', 'd_high_12', 'd_low_12',
                                 'd_high_13', 'd_low_13', 'd_high_14',
                                 'd_low_14', 'd_high_15', 'd_low_15',
                                 'd_wea_1', 'd_wea_2', 'd_wea_3',
                                 'd_wea_4', 'd_wea_5', 'd_wea_6',
                                 'd_wea_7', 'd_wea_8', 'd_wea_9',
                                 'd_wea_10', 'd_wea_11', 'd_wea_12',
                                 'd_wea_13', 'd_wea_14', 'd_wea_15'])
        df.to_csv(f'weather_data/new_{file}', index=False, header=False)

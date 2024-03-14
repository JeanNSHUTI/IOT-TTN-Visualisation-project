import math

import pandas as pd
import numpy as np

#df_h25ka = pd.read_csv('hk_humidity_table.csv')


def find_column(temp):
    for x in range(0, 50, 5):
        if temp < x:
            col2 = x
            col1 = x-5
            return col1, col2


def create_new_col(temp):
    col1, col2 = find_column(temp)
    col_temp = str(temp) + "°C"
    col_temp_prev = str(col1) + "°C"
    col_temp_next = str(col2) + "°C"
    df_h25ka = pd.read_csv('hk_humidity_table.csv')
    if col_temp not in df_h25ka.columns.values:
        df_h25ka.insert((col1//5)+1, col_temp, np.nan)
        df_h25ka[col_temp] = df_h25ka.apply(lambda row: row[col_temp_prev] + (((temp - col1)/5) * (row[col_temp_next] - row[col_temp_prev]))
                       , axis=1)

    return df_h25ka, col_temp


def calculate_rh_value(temp, m_resistance):
    m_resistance = int(m_resistance)
    dataframe, col_temp = create_new_col(temp)
    rh_percent = 20
    next_resistance = next_rh_percent = prev_resistance = prev_rh_percent = 0

    for resistance in dataframe[col_temp]:
        if resistance < m_resistance and resistance != 0:
            next_resistance = resistance
            next_rh_percent = rh_percent
            break
        prev_resistance = resistance
        prev_rh_percent = rh_percent
        rh_percent = rh_percent + 5

#    print(next_resistance)
#    print(prev_resistance)

    result_rh_percent = prev_rh_percent + (((m_resistance - prev_resistance) / (next_resistance-prev_resistance)) *
                                           (next_rh_percent-prev_rh_percent))
    return round(result_rh_percent)


def calculate_temperature(mvolt):
    mvolt = int(mvolt)
    temp_celsius = ((5.506 - math.sqrt(pow(-5.506, 2) + (4 * 0.00176 * (870.6 - mvolt)))) / (2 * (-0.00176))) + 30
    return round(temp_celsius, 2)


def calculate_lum(mvolt):
    print(mvolt)
    mvolt = int(mvolt)
    volt = mvolt / 1000.0
    luminosity_percentage = (volt/3.3) * 100.0
    return round(luminosity_percentage)


def calculate_hum_resistance(mvolt):
    print(mvolt)
    mvolt = int(mvolt)
    volt = mvolt/1000.00  # Get volt
    if volt > 0:
        hum_resistance_kohms = ((3.3/volt) - 1.0) * 47.0
        return hum_resistance_kohms
    


#rh = calculate_rh_value(8, 5000)
#print(rh)

#print(calculate_temperature(912.9))

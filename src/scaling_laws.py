"""
Functions for verifying the scaling laws
"""


from intrinsic_time import calc_intrinsic_events, DC_UP, DC_DOWN, NE, OS_UP, OS_DOWN
import numpy as np


def calc_avg_os(df, th_up, th_down):
    """
    function to calculate average overshoot length given a data series and a threshold (up, down)

    :param df: DataFrame with columns: ['Datetime', 'Value']
    :param th_up: directional change threshold upward
    :param th_down: directional change threshold downward
    :return: (df_out, list_os, avg_os_abs)
            df_out: DataFrame with columns: ['Datetime', 'Value', 'IE']
    """
    df = df.sort_values(by='Datetime')
    df['IE'] = calc_intrinsic_events(list_prices_series=df['Value'], threshold_up=th_up, threshold_down=th_down)
    list_os = []
    count = 0
    df_ie = df[df['IE'] != NE]
    for (index, row) in df_ie.iterrows():
        price = row['Value']
        ie = row['IE']
        if count == 0:  # initialization
            previous_ie_price = price
            price_os_start = price
        if ie in [DC_UP, DC_DOWN]:  # if directional change, take previous event price as end of overshoot
            price_os_end = previous_ie_price
            os = price_os_end - price_os_start
            list_os.append(os)
            price_os_start = price  # reset start price of overshoot
            previous_ie_price = price
        elif ie in [OS_UP, OS_DOWN]:
            previous_ie_price = price
        else:
            pass
        count = count + 1
    avg_os = np.mean([abs(x) for x in list_os])
    return df, list_os, avg_os






"""
This module contains functions for data loading
"""
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt


def load_data_jforex(file_dir, file_name):
    """
    :param file_dir:
    :param file_name: a csv file containing tick-by-tick data downloaded from
                        JForex. e.g.: AUDCAD_Ticks_2019.03.11_2019.03.13.csv
    :return: df, with columns: Datetime, Ask, Bid, AskVolume, BidVolume
    """
    file = os.path.join(file_dir, file_name)
    df = pd.read_csv(file)
    df['Datetime'] = pd.to_datetime(df['Time (UTC)'])
    return df



# todo: cannot read a 5GB csv file
# Try something like this:
# chunksize = 10 ** 6
# for chunk in pd.read_csv(filename, chunksize=chunksize):
#     process(chunk)

def load_data_jforex_by_chunk(file_dir, file_name):
    """
    :param file_dir:
    :param file_name: a csv file containing tick-by-tick data downloaded from
                        JForex. e.g.: AUDCAD_Ticks_2019.03.11_2019.03.13.csv
    :return: df, with columns: Datetime, Ask, Bid, AskVolume, BidVolume
    """
    file = os.path.join(file_dir, file_name)
    chunksize = (10 ** 6)
    df = pd.DataFrame()
    for chunk in pd.read_csv(file, chunksize=chunksize):
        print('reading only first chunk')
        chunk['Datetime'] = pd.to_datetime(chunk['Time (UTC)'])
        print(chunk['Datetime'].max())
        return chunk
    # return df #todo: tmp test



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



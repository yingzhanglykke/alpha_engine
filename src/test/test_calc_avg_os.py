from unittest import TestCase

from config import ConfigScalingLawTesting
from dal import load_data_jforex
from scaling_laws import calc_avg_os
import math
import matplotlib.pyplot as plt
import pandas as pd
import pickle


class TestCalc_avg_os(TestCase):
    def test_calc_avg_os(self):
        # prepare data
        file_dir = ConfigScalingLawTesting.data_path
        file_name = ConfigScalingLawTesting.file_name_test_jforex_two_days
        df = load_data_jforex(file_dir, file_name)
        df['Value'] = df['Ask']
        df = df[['Datetime', 'Value']]
        # define a list of threshold
        min_th = 0.0001
        max_th = 0.1
        nr_points = 10
        incre = (math.log(max_th) - math.log(min_th))/(nr_points - 1)
        list_th = [math.exp(math.log(min_th) + i * incre) for i in range(nr_points)]
        # calculate avg_os
        list_avg_os = []
        list_list_os = []
        for th in list_th:
            df_out, list_os, avg_os = calc_avg_os(df=df, th_up=th, th_down=th)
            list_avg_os.append(avg_os)
            list_list_os.append(list_os)
        print(list_th)
        print(list_avg_os)

        # save output in a DataFrame and pickle
        df_out_aggr = pd.DataFrame()
        df_out_aggr['th'] = list_th
        df_out_aggr['list_os'] = list_list_os
        df_out_aggr['avg_os'] = list_avg_os
        with open('output_avg_os.pickle', 'wb') as f:
            pickle.dump(df_out_aggr, f, pickle.HIGHEST_PROTOCOL)


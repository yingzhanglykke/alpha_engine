from unittest import TestCase

from config import ConfigScalingLawTesting
from dal import load_data_jforex
from scaling_laws import calc_avg_os
import math
import matplotlib.pyplot as plt


class TestCalc_avg_os(TestCase):
    def test_calc_avg_os(self):
        # prepare data
        file_dir = ConfigScalingLawTesting.data_path
        file_name = ConfigScalingLawTesting.file_name_test_jforex
        df = load_data_jforex(file_dir, file_name)
        df['Value'] = df['Ask']
        df = df[['Datetime', 'Value']]
        # define a list of threshold
        min_th = 0.0001
        max_th = 0.1
        nr_points = 4
        incre = (math.log(max_th) - math.log(min_th))/(nr_points - 1)
        list_th = [math.exp(math.log(min_th) + i * incre) for i in range(nr_points)]
        # calculate avg_os
        list_avg_os = []
        for th in list_th:
            df_out, list_os, avg_os = calc_avg_os(df=df, th_up=th, th_down=th)
            list_avg_os.append(avg_os)
        print(list_th)
        print(list_avg_os)

        plt.subplot(2, 1, 1)
        plt.scatter(list_th, list_avg_os)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(((1e-5, 0.1)))
        plt.ylim((1e-5, 0.1))
        plt.show()

    def test_plot(self):
        a = [0.00010000000000000009, 0.0002154434690031884, 0.0004641588833612784, 0.0010000000000000002, 0.0021544346900318864, 0.004641588833612781, 0.010000000000000004, 0.02154434690031885, 0.046415888336127815, 0.10000000000000006]

        b = [8.836491608012956e-05, 0.00018201923076922811, 0.00037232558139535326, 0.0005068421052631535, 0.00040999999999999923, 0.0, 0.0, 0.0, 0.0, 0.0]
        plt.subplot(2, 1, 1)
        plt.scatter(a, b)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(((1e-5, 0.1)))
        plt.ylim((1e-5, 0.1))
        plt.show()
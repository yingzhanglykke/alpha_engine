from unittest import TestCase

from scaling_laws import calc_log_regression
import pickle


class TestCalc_log_regression(TestCase):
    def test_calc_log_regression(self):
        a = [0.00010000000000000009, 0.0002154434690031884, 0.0004641588833612784, 0.0010000000000000002,
             0.0021544346900318864, 0.004641588833612781, 0.010000000000000004, 0.02154434690031885,
             0.046415888336127815, 0.10000000000000006]
        b = [8.836491608012956e-05, 0.00018201923076922811, 0.00037232558139535326, 0.0005068421052631535,
             0.00040999999999999923, 0.0, 0.0, 0.0, 0.0, 0.0]
        calc_log_regression(a, b)

    def test_calc_log_regression_with_pickled_os_data(self):
        with open('output_avg_os.pickle', 'rb') as f:
            df_out_aggr = pickle.load(f)
        print(df_out_aggr)
        a = df_out_aggr['th']
        b = df_out_aggr['avg_os']
        calc_log_regression(a, b)

from unittest import TestCase

from config import ConfigScalingLawTesting
from dal import load_data_jforex
import matplotlib.pyplot as plt
from intrinsic_time import calc_intrinsic_events, NE


class TestCalc_intrinsic_events(TestCase):
    def test_calc_intrinsic_events(self):
        file_dir = ConfigScalingLawTesting.data_path
        file_name = ConfigScalingLawTesting.file_name_test_jforex_two_days
        df = load_data_jforex(file_dir, file_name)
        # plot
        ax = plt.gca()
        df.plot(x='Datetime', y='Ask', ax=ax)
        for th in [0.0001, 0.0005, 0.001, 0.002, 0.003, 0.005]:
            df['IE'] = calc_intrinsic_events(df['Ask'], th, th)
            df_intrinsic = df[df['IE'] != NE]
            df_intrinsic.plot(x='Datetime', y='Ask', ax=ax)
        plt.show()


    def test_calc_intrinsic_events_four_year_data(self):
        file_dir = ConfigScalingLawTesting.data_path
        file_name = ConfigScalingLawTesting.file_name_test_jforex_four_year
        df = load_data_jforex(file_dir, file_name)
        # plot
        ax = plt.gca()
        df.plot(x='Datetime', y='Ask', ax=ax)
        for th in [0.005]:
            df['IE'] = calc_intrinsic_events(df['Ask'], th, th)
            df_intrinsic = df[df['IE'] != NE]
            df_intrinsic.plot(x='Datetime', y='Ask', ax=ax)
        plt.show()

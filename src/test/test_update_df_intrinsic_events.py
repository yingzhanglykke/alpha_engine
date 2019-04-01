from unittest import TestCase

from config import ConfigScalingLawTesting
from dal import load_data_jforex
import matplotlib.pyplot as plt

from intrinsic_time_v2 import L_MIN, update_df_intrinsic_events, DC, L_MAX


class TestUpdate_df_intrinsic_events(TestCase):
    def test_update_df_intrinsic_events(self):
        file_dir = ConfigScalingLawTesting.data_path
        file_name = ConfigScalingLawTesting.file_name_test_jforex_two_days
        df = load_data_jforex(file_dir, file_name)
        # plot
        ax = plt.gca()
        df.plot(x='Datetime', y='Ask', ax=ax)
        # list_ths = [0.0001, 0.0005, 0.001]
        list_ths = [0.0005]
        for th in list_ths:
            th_up = th
            th_down = th
            # initialization
            df_ie = None
            local_ext_time = df['Datetime'].iloc[0]
            local_ext_type = L_MIN
            local_ext_value = df['Ask'].iloc[0]
            for i in range(len(df)):
                new_time = df['Datetime'].iloc[i]
                new_value = df['Ask'].iloc[i]
                df_ie, local_ext_time, local_ext_type, local_ext_value = \
                    update_df_intrinsic_events(df_ie, new_time, new_value, local_ext_time, local_ext_type,
                                               local_ext_value, th_up, th_down)


            df_ie.plot(x='Datetime', y='Value', ax=ax)
            # plot directional change point
            df_DC = df_ie[df_ie['IE'] == DC]
            df_DC.plot(x='Datetime', y='Value', ax=ax, style=".")
            # plot local ext
            df_ext = df_ie[df_ie['IE'].isin([L_MIN, L_MAX])]
            df_ext.plot(x='Datetime', y='Value', ax=ax, style=".")
        plt.show()

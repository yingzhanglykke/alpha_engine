import pickle
from unittest import TestCase

from intrinsic_time import plot_intrinsic_events


class TestPlot_intrinsic_events(TestCase):
    def test_plot_intrinsic_events(self):
        with open('output_avg_os.pickle', 'rb') as f:
            df_out_aggr = pickle.load(f)
        print(df_out_aggr)
        a = df_out_aggr['th']
        b = df_out_aggr['avg_os']
        c = df_out_aggr['list_tuple_ie']
        plot_intrinsic_events(c[0])

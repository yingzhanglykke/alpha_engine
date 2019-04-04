import cProfile
import math
import os
import pickle

from config import ConfigScalingLawTesting
from os_scaling_law import run_os_scaling_law

pickle_file = 'output_avg_os.pickle'


def calc_os():
    file_dir = ConfigScalingLawTesting.data_path
    # file_name = ConfigScalingLawTesting.file_name_test_jforex_two_days
    # file_name = ConfigScalingLawTesting.file_name_test_jforex_four_year
    file_name = ConfigScalingLawTesting.file_name_test_jforex_four_year_copy

    file = os.path.join(file_dir, file_name)
    th_min = 0.0001
    th_max = 0.0505
    nr_points = 250
    max_nr_rows = 1e9
    # split into N part
    incre = (math.log(th_max) - math.log(th_min)) / (nr_points - 1)
    list_th = [math.exp(math.log(th_min) + i * incre) for i in range(nr_points)]
    N = 50
    for i in range(N):
        min = list_th[i * int(nr_points / N)]
        max = list_th[(i+1) * int(nr_points / N) - 1]
        pickle_file = 'output//output_avg_os_part{}_{}e6_rows.pickle'.format(i, int(max_nr_rows/1e6))
        run_os_scaling_law(file, min, max, int(nr_points / N), output_file=pickle_file, max_nr_rows=max_nr_rows)

if __name__ == '__main__':
    # cProfile.run('calc_os()')
    calc_os()
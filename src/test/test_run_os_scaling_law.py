import cProfile
import os
from unittest import TestCase

from config import ConfigScalingLawTesting
from os_scaling_law import run_os_scaling_law


class TestRun_os_scaling_law(TestCase):
    def test_run_os_scaling_law(self):
        file_dir = ConfigScalingLawTesting.data_path
        file_name = ConfigScalingLawTesting.file_name_test_jforex_two_days
        # file_name = ConfigScalingLawTesting.file_name_test_jforex_four_year
        file = os.path.join(file_dir, file_name)
        th_min = 0.0001
        th_max = 0.001
        nr_points = 200
        # run
        run_os_scaling_law(file, th_min, th_max, nr_points, max_nr_rows=1e7)

    def test_mp(self):
        import multiprocessing as mp
        print("Number of processors: ", mp.cpu_count())
        def f(x):
            x = x+1
            return x, x+1
        pool = mp.Pool(mp.cpu_count())
        pool.map(f, [2,3,4])


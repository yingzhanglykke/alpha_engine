"""
This module provides the function to calculate the avg overshooting length for
a JForex dataset (csv) file
"""
import csv
import datetime
import math
import pickle
import pandas as pd

from intrinsic_time import L_MIN, update_df_intrinsic_events, calc_avg_os

def run_os_scaling_law(data_file, min_th, max_th, nr_points,
                       output_file='output_avg_os.pickle',
                       max_nr_rows=1e9,
                       time_col_name='Time (UTC)',
                       price_col_name='Ask'):
    """
    :param data_file:
    :param min_th:
    :param max_th:
    :param nr_points:
    :param max_nr_rows: max number of rows to process
    :param output_file: full path and name for output pickle file
    :param time_col_name:
    :param price_col_name:
    :return:
    """
    # define a list of threshold
    if nr_points == 1:
        incre = 0
    else:
        incre = (math.log(max_th) - math.log(min_th)) / (nr_points - 1)
    list_th = [math.exp(math.log(min_th) + i * incre) for i in range(nr_points)]

    # profiling
    start_time = datetime.datetime.now()

    # open csv file and perform calc for the list_th
    with open(data_file) as csv_file:
        print("file opened")
        list_list_tuple_ie = [None] * len(list_th)

        # option 2: faster than csv.reader
        for line_count, r in enumerate(csv_file):
            row = r[:-1].split(',')
            # break if line_count excceds max_nr_rows
            if line_count > max_nr_rows:
                break

            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                idx_time_col = row.index(time_col_name)
                idx_price_col = row.index(price_col_name)
            elif line_count == 1:
                # initialization
                print("initilization")
                list_local_ext_time = [row[idx_time_col]] * len(list_th)
                list_local_ext_type = [L_MIN] * len(list_th)
                list_local_ext_value = [float(row[idx_price_col])] * len(list_th)
            else:
                new_time = row[idx_time_col]
                new_value = float(row[idx_price_col])  # 'Ask'
                
                for i in range(len(list_th)):
                    th = list_th[i]
                    list_list_tuple_ie[i], list_local_ext_time[i], list_local_ext_type[i], list_local_ext_value[i] = \
                            update_df_intrinsic_events(list_list_tuple_ie[i], new_time, new_value, list_local_ext_time[i],
                                                       list_local_ext_type[i], list_local_ext_value[i], th, th)

                # print progress in console
                if line_count % 1e6 == 0:
                    now = datetime.datetime.now()
                    print('running {}th row. time spent{}'.format(line_count, now-start_time))
                    start_time = now

    # calculate avg_os
    dict_list_tuple_ie = dict(zip(list_th, list_list_tuple_ie))
    dict_avg_os = dict()
    for th in list_th:
        list_os, avg_os_abs = calc_avg_os(dict_list_tuple_ie[th])
        dict_avg_os.update({th: avg_os_abs})
    print(dict_avg_os)

    # save output in a DataFrame and pickle
    df_out_aggr = pd.DataFrame()
    df_out_aggr['th'] = list_th
    ## list_tuple_ie is too big to pickle
    # df_out_aggr['list_tuple_ie'] = [dict_list_tuple_ie[th] for th in list_th]
    df_out_aggr['avg_os'] = [dict_avg_os[th] for th in list_th]
    with open(output_file, 'wb') as f:
        pickle.dump(df_out_aggr, f, pickle.HIGHEST_PROTOCOL)

    return df_out_aggr



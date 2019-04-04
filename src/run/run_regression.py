import pickle

from log_regression import calc_log_regression


def run_regression():
    # specify nr of parts
    N = 50
    max_nr_rows = 1e9
    df_out_aggr = None
    for i in range(N):
        pickle_file = 'output//output_avg_os_part{}_{}e6_rows.pickle'.format(i, int(max_nr_rows/1e6))

        try:
            with open(pickle_file, 'rb') as f:
                df_out_aggr_part = pickle.load(f)
            df_out_aggr = df_out_aggr_part if df_out_aggr is None else df_out_aggr.append(df_out_aggr_part, ignore_index=True)
        except:
            print("file not found")
    a = df_out_aggr['th']
    b = df_out_aggr['avg_os']
    calc_log_regression(a, b)

if __name__ == '__main__':
    run_regression()

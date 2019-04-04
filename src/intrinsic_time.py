"""
This module contains the function to update the intrisic_event DataFrame given a new tick-by-tick data point for
a given threshold (th_up, th_down)
"""
import datetime

import pandas as pd
import matplotlib.pyplot as plt

L_MIN = 'local_min'
L_MAX = 'local_max'
DC = 'directional_change'


def update_df_intrinsic_events(list_tuple_ie, new_time, new_value, local_ext_time, local_ext_type,
                               local_ext_value, th_up, th_down):
    """

    :param list_tuple_ie: [('Datetime', 'Value', 'IE'),(),.]
                'IE' can be one of (L_MIN, L_MAX, DC)
    :param new_time:
    :param new_value:
    :param local_ext_time:
    :param local_ext_type:
    :param local_ext_value:
    :param th_up:
    :param th_down:
    :return: list_tuple_ie (updated), local_ext_time, local_ext_type, local_ext_value
    """
    # initialization
    NEW_DC = 'NEW_DC'
    UPDATE_L_EXT = 'UPDATE_L_EXT'
    NO_UPDATE = 'NO_UPDATE'

    # calculate status
    if local_ext_type == L_MAX:
        # # profiling
        # start_time = datetime.datetime.now()
        # print(start_time)

        if new_value >= local_ext_value:  # register new local_ext, no update in list_tuple_ie
            status = UPDATE_L_EXT
            # # profiling
            # end_time = datetime.datetime.now()
            # print(end_time - start_time)
        elif new_value <= local_ext_value * (1 - th_down):  # directional change: update list_tuple_ie, local_ext
            status = NEW_DC
            # # profiling
            # end_time = datetime.datetime.now()
            # print(end_time - start_time)
        else:
            status = NO_UPDATE
        # # profiling
        # end_time = datetime.datetime.now()
        # print(end_time - start_time)

    elif local_ext_type == L_MIN:
        if new_value <= local_ext_value:  # register new local_ext
            status = UPDATE_L_EXT
        elif new_value >= local_ext_value * (1 + th_up):  # directional change
            status = NEW_DC
        else:
            status = NO_UPDATE
    else:
        raise ValueError

    # output for different status
    if status == UPDATE_L_EXT:  # register new local_ext, no update in list_tuple_ie
        local_ext_value = new_value
        local_ext_time = new_time
    elif status == NEW_DC:  # directional change: update list_tuple_ie, local_ext
        if list_tuple_ie is None:
            list_tuple_ie = []
        row1 = (local_ext_time, local_ext_value, local_ext_type)
        row2 = (new_time, new_value, DC)
        list_tuple_ie.append(row1)
        list_tuple_ie.append(row2)

        # update local_ext
        local_ext_type = L_MIN if local_ext_type == L_MAX else L_MAX
        local_ext_value = new_value
        local_ext_time = new_time
    else:
        pass

    # print("single row update takes {}".format(end_time - start_time))
    return list_tuple_ie, local_ext_time, local_ext_type, local_ext_value



def calc_avg_os(list_tuple_ie):
    """

    :param list_tuple_ie: [('Datetime', 'Value', 'IE'),(),.];
                'IE' can be one of (L_MIN, L_MAX, DC)
    :return: list_os, avg_os_abs
    """
    col_names = ['Datetime', 'Value', 'IE']
    df_ie = pd.DataFrame(list_tuple_ie, columns=col_names)
    df_ie['Value_previous_IE'] = df_ie['Value'].shift(1)
    df_ie_os = df_ie[df_ie['IE'].isin([L_MIN, L_MAX])]
    df_ie_os['os'] = df_ie_os['Value'] - df_ie_os['Value_previous_IE']
    list_os = df_ie_os['os']
    avg_os_abs = df_ie_os['os'].abs().mean()
    return list_os, avg_os_abs


def plot_intrinsic_events(list_tuple_ie):
    """

    :param list_tuple_ie: list_tuple_ie: [('Datetime', 'Value', 'IE'),(),.];
                'IE' can be one of (L_MIN, L_MAX, DC)
    :return:
    """
    col_names = ['Datetime', 'Value', 'IE']
    df_ie = pd.DataFrame(list_tuple_ie, columns=col_names)
    df_ie['Datetime'] = pd.to_datetime(df_ie['Datetime'])

    ax = plt.gca()
    df_ie.plot(x='Datetime', y='Value', ax=ax)
    # plot directional change point
    df_DC = df_ie[df_ie['IE'] == DC]
    df_DC.plot(x='Datetime', y='Value', ax=ax, style=".", label='directional_change', color='red')
    # plot local ext
    df_ext = df_ie[df_ie['IE'].isin([L_MIN, L_MAX])]
    df_ext.plot(x='Datetime', y='Value', ax=ax, style=".", label='local_ext', color='blue')
    plt.show()

"""
This module contains the function to update the intrisic_event DataFrame given a new tick-by-tick data point for
a given threshold (th_up, th_down)
"""
import pandas as pd

L_MIN = 'local_min'
L_MAX = 'local_max'
DC = 'directional_change'


def update_df_intrinsic_events(df_ie, new_time, new_value, local_ext_time, local_ext_type,
                               local_ext_value, th_up, th_down):
    """

    :param df_ie: ['Datetime', 'Value', 'IE'];
                'IE' can be one of (L_MIN, L_MAX, DC)
    :param new_time:
    :param new_value:
    :param local_ext_time:
    :param local_ext_type:
    :param local_ext_value:
    :param th_up:
    :param th_down:
    :return: df_ie (updated), local_ext_time, local_ext_type, local_ext_value
    """
    # initialization
    NEW_DC = 'NEW_DC'
    UPDATE_L_EXT = 'UPDATE_L_EXT'
    NO_UPDATE = 'NO_UPDATE'

    # calculate status
    if local_ext_type == L_MAX:
        if new_value >= local_ext_value:  # register new local_ext, no update in df_ie
            status = UPDATE_L_EXT
        elif new_value <= local_ext_value * (1 - th_down):  # directional change: update df_ie, local_ext
            status = NEW_DC
        else:
            status = NO_UPDATE
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
    if status == UPDATE_L_EXT:  # register new local_ext, no update in df_ie
        local_ext_value = new_value
        local_ext_time = new_time
    elif status == NEW_DC:  # directional change: update df_ie, local_ext
        df_new_ies = pd.DataFrame()
        df_new_ies['Datetime'] = [local_ext_time, new_time]
        df_new_ies['Value'] = [local_ext_value, new_value]
        df_new_ies['IE'] = [local_ext_type, DC]
        df_ie = df_ie.append(df_new_ies, ignore_index=True) if df_ie is not None else df_new_ies
        # update local_ext
        local_ext_type = L_MIN if local_ext_type == L_MAX else L_MAX
        local_ext_value = new_value
        local_ext_time = new_time
    else:
        pass

    return df_ie, local_ext_time, local_ext_type, local_ext_value

"""
Functions for verifying the scaling laws
"""
from sklearn.metrics import mean_squared_error, r2_score

from intrinsic_time import calc_intrinsic_events, DC_UP, DC_DOWN, NE, OS_UP, OS_DOWN
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model, datasets
import math
import pandas as pd


def calc_avg_os(df, th_up, th_down):
    """
    function to calculate average overshoot length given a data series and a threshold (up, down)

    :param df: DataFrame with columns: ['Datetime', 'Value']
    :param th_up: directional change threshold upward
    :param th_down: directional change threshold downward
    :return: (df_out, list_os, avg_os_abs)
            df_out: DataFrame with columns: ['Datetime', 'Value', 'IE']
    """
    df = df.sort_values(by='Datetime')
    df['IE'] = calc_intrinsic_events(list_prices_series=df['Value'], threshold_up=th_up, threshold_down=th_down)
    list_os = []
    count = 0
    df_ie = df[df['IE'] != NE]
    for (index, row) in df_ie.iterrows():
        price = row['Value']
        ie = row['IE']
        if count == 0:  # initialization
            previous_ie_price = price
            price_os_start = price
        if ie in [DC_UP, DC_DOWN]:  # if directional change, take previous event price as end of overshoot
            price_os_end = previous_ie_price
            os = price_os_end - price_os_start
            list_os.append(os)
            price_os_start = price  # reset start price of overshoot
            previous_ie_price = price
        elif ie in [OS_UP, OS_DOWN]:
            previous_ie_price = price
        else:
            pass
        count = count + 1
    avg_os = np.mean([abs(x) for x in list_os])
    return df, list_os, avg_os



def calc_log_regression(list_stat_x, list_stat_y, fig_file_name = None):
    """
    :param list_stat_x:
    :param list_stat_y:
    :param fig_file_name: file name for saved plot
    :return:
    """
    # regression analysis
    # prepare data
    df = pd.DataFrame()
    df['x'] = list_stat_x
    df['y'] = list_stat_y
    df['x_log'] = np.log(df['x'])
    df['y_log'] = np.log(df['y'])
    df_new = df.replace([np.inf, -np.inf], np.nan).dropna()

    # Create linear regression object
    regr = linear_model.LinearRegression()
    x = df_new[['x_log']]
    y = df_new['y_log']
    regr.fit(x, y)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"% mean_squared_error(x, y))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(x, y))

    # log plot
    plt.scatter(list_stat_x, list_stat_y, color='black')
    # Make predictions using the testing set (for drawing the line)
    x_pred = x
    y_pred = regr.predict(x)
    plt.plot([math.exp(i) for i in x_pred['x_log']], [math.exp(i) for i in y_pred], color='blue', linewidth=3)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlim((1e-5, 0.1))
    plt.ylim((1e-5, 0.1))

    fig_file_name = 'output.png' if fig_file_name is None else fig_file_name
    plt.savefig(fig_file_name)
    plt.show()



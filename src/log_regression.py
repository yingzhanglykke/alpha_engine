import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


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
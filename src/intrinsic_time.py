"""
This module contains the function to convert tick-by-tick data to a list of intrinsic events DC / OS for a
given threshold
"""

DC_UP = 'Directional Change Upward'
DC_DOWN = 'Directional Change Downward'
OS_UP = 'Overshoot Upward'
OS_DOWN = 'Overshoot Downward'
NE = 'No Event'

def calc_intrinsic_events(list_prices_series, threshold_up, threshold_down):
    """

    :param list_prices_series: e.g. tick-by-tick price data
    :return: list_intrinsic events
    """
    list_intrinsic_events = []
    for i in range(len(list_prices_series)):
        current_price = list_prices_series[i]
        if i == 0:
            event = DC_DOWN  # assume downward directional change for the first price
        else:
            if previous_event in [DC_UP, OS_UP]:
                if current_price > previous_price:
                    event = OS_UP
                elif current_price < previous_price * (1 - threshold_down):
                    event = DC_DOWN
                else:
                    event = NE
            elif previous_event in [DC_DOWN, OS_DOWN]:
                if current_price < previous_price:
                    event = OS_DOWN
                elif current_price > previous_price * (1 + threshold_up):
                    event = DC_UP
                else:
                    event = NE
            else:
                raise ValueError
        previous_event = event if event != NE else previous_event
        previous_price = current_price if event != NE else previous_price
        list_intrinsic_events.append(event)
    return list_intrinsic_events




"""
This Module is created to backtest given strategies agains past courses.
"""

import datetime
import Main
import Supporter
import pandas as pd

from Data_access_ystockquote import get_price_data


def backtest(ref, *args):
    """
    Tests if your investment idea works. You need to enter at least one reference (more not implemented yet)
    and it you can set a timerange (int, a day each) by the keyword timerange
    """
    date = datetime.date.today()
    if "timerange" in kwargs:
        timeline = datetime.timedelta(kwargs["timerange"])
    else:
        timeline = datetime.timedelta(200) #Default value
    start = date - timeline
    reference = get_price_data(ref, start.isoformat(), date.isoformat())
    Supporter.show_values(reference["High"])


def backtest_stockpup(ref, *args):
    """
    Tests if your investment idea works. You need to enter at least one reference (more not implemented yet)
    and it you can set a timerange (int, a day each) by the keyword timerange
    """
    date = datetime.date.today()
    datelist = pd.date_range(pd.datetime.today(), periods=100).tolist()
    start = date - timeline
    reference = get_price_data(ref, start.isoformat(), date.isoformat())
    Supporter.show_values(reference["High"])


if __name__ == "__main__":
    backtest_stockpup("GSPC", timerange = 100)

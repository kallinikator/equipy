"""
This Module is created to backtest given strategies agains past courses.
"""

import datetime
import Main
import Supporter

from Data_access_ystockquote import get_price_data


def backtest(ref, *args, **kwargs):
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


if __name__ == "__main__":
    backtest("GSPC", timerange = 100)
    backtest("AAPL")
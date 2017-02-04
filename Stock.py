#coding=utf-8

import pandas as pd
from Yahoo import query


class Stock(object):
    """
    The base class for stock objects. Inheritants contain specifications depending on your data-source.
    """
    def __init__(self):   
        self.score = 0
        self.complete_pricelist = True

    def __repr__(self):
        return "A Share-Object of {}, its score is {}.".format(self.name, self.score)

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score > other.score    

    def __ge__(self, other):
        return self.score >= other.score


class Stock_Stockpup(Stock):
    """
    Creates a share-object from the data from stockpup. This object can calculate
    different scores and the correlation of its value to those scores
    """

    def __init__(self, symbol, *args):
        super().__init__()

        self.data = pd.read_csv(open(r"Stock_Data/{}.csv".format(symbol)))
        self.data = self.data.apply(pd.to_numeric, errors="ignore")
        self.data.index = self.data["Quarter end"]
        self.name = symbol

        if self.data["Price"].dtype in (int, float) and self.data["Cumulative dividends per share"].dtype in (int, float):
            self.data["Value"] = self.data["Price"] + self.data["Cumulative dividends per share"]
            # Calculation of the estimated return
            self.data["Estimated Return"] = self.data["Value"].pct_change()
            # Calculation of the standard deviation
            self.data["Standard Deviation"] = self.data["Value"].std()
        else:
            self.complete_pricelist = False

    def __len__(self):
        return len(self.data.index)


class Stock_Yahoo(Stock):
    """
    Creates a share-object from the date from Yahoo. You will need internet access, since the data are pulled live for yahoo.
    """

    def __init__(self, symbol, *args, **kwargs):
        super().__init__()
        self.data = query(symbol)["query"]["results"]["quote"]
        self.name = symbol


if __name__ == "__main__":
    Y = Stock_Stockpup("AA")

    # TODO Unittest
    # TODO Too short or too incomplete Information are ignored. Maybe I find a better way to gather them!

#coding=utf-8

import pandas
import math

from Yahoo import query


class Stock(object):
    """
    Base class for stck objects. Inheritants contain specifications depending on your data-source.
    """
    def __init__(self):   
        self.score = 0
        self.name = ""

    # Only some misc stuff
    def __repr__(self):
        return "A Share-Object of {}, its score is {}.".format(self.name, self.score)

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score > other.score    

    def __ge__(self, other):
        return self.score >= other.score

    def __se__(self, other):
        return self.score < other.score

    def __st__(self, other):
        return self.score <= other.score

    def get_info(self):
        print("This is a share of {}\n{}\nIt is score is {}".format(self.name, self.data, self.score))


class Stock_Stockpup(Stock):
    """
    Creates a share-object from the data from stockpup. This object can calculate
    different scores and the correlation of its value to those scores
    """

    def __init__(self, symbol, timeline = '3J'):
        super().__init__()
        # What is this- I forgot but it only works with 12..     
        self.data = pandas.read_csv(open(r"Stockpup/{0}/{0}.csv".format(symbol + "_quarterly_financial_data"))).head(12) 
        self.data = self.data.iloc[::-1].convert_objects(convert_numeric = True) # Converts all values from string to integers and turn around
        self.data.index = pandas.date_range(periods = 12, end = "2015-12-31", freq = "3M")
        self.name = symbol
        self.score = 0

        #Ugly solution: TODO find a better way to filter out unwanted data
        try:
            for category in ["ROE", "Revenue", "Earnings", "Equity to assets ratio", "P/E ratio", "Price", "EPS basic"]:
                self.data[category] + 1 # Filters out because if a category doesnt exist or ist an integer, it will break
        except:
            print("Data Corrupted at {} at {}".format(self.name, category))
            raise Exception("Data Corrupted at {} at {}".format(self.name, category))

        for category in ["ROE", "Revenue", "Earnings", "Equity to assets ratio", "P/E ratio", "Price", "EPS basic"]:
            if math.isnan(self.data[category][-1]):
                print("Data Incomplete at {} at {}".format(self.name, category))
                raise Exception("Data Incomplete at {} at {}".format(self.name, category))

        # Calculation of the estimated return 
        self.data["Estimated Return"] = self.data["Price"].pct_change() # TODO This is not taking dividents into account!
        # Calculation of the standard deviation
        self.data["Standard Deviation"] = self.data["Price"].std()


class Stock_Yahoo(Stock):
    """
    Creates a share-object from the date from Yahoo. You will need internet access, since the data are pulled live in this stadium.
    """

    def __init__(self, symbol, *args, **kwargs):
        super().__init__()
        self.data = query(symbol)


if __name__ == "__main__":
    Y = Stock_Yahoo("GOOG")

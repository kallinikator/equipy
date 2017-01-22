#coding=utf-8

import pandas as pd
import glob
import math

import Stock


# TODO deal with wrong or incomplete data

class Portfolio(object):
    """
    Creates the optimal portfolio from a given universe of stocks. This is a base class for all kind of freely
    configurable strategies
    """
    def __init__(self, folder="Stock_Data"):
        self.stocklist = []
        self.create_stocklist(folder)

    def create_stocklist(self, folder, maxcounter=20, **kwargs):
        """
        Creates the stocklist for this Portfolio by iterating through existing data.
        """
        counter = 0
        # Only for testing reasons, limits the number of used stocks to a given number
        # Creates all shares as Stock-objects
        for share in glob.glob(folder + "/*.csv"):
            symbol = share.split("\\")[-1].split(".")[0]
            self.stocklist.append(Stock.Stock_Stockpup(symbol))

            # Only for testing reasons!
            counter += 1
            if counter >= maxcounter:
                break

    def rate(self, category, border=0.2, score=1, positive=True, debug=True):
        """
        This Function is uses to find the best and the worst 20 percent in a given category.
        """
        borderlist = [category(stock) for stock in self.stocklist if not math.isnan(category(stock))]
        borderlist.sort(reverse=True)
        borders = (borderlist[round(len(borderlist)*border)], borderlist[round(len(borderlist)*(1-border))])
        # Rating part
        for stock in self.stocklist:
            if positive:
                if category(stock) > borders[0]:
                    stock.score += score
                if category(stock) < borders[1]:
                    stock.score -= score
            else: 
                if category(stock) > borders[1]:
                    stock.score += score
                if category(stock) < borders[0]:
                    stock.score -= score
            if debug: # Allows for further information
                print("Stock:\t{}\nValue:\t{}\nNew rating:\t{}".format(stock.name, category(stock), stock.score))

    def show_result(self):
        for stock in self.stocklist:
            print(stock)

class MyFirstStrategy(Portfolio):
    """
    This Strategy is implemented as a rating system similar to the ideas of Susam Levermann. In difference to her ideas,
    this strategy is much more diversified (higher amount of stocks) and doesn´t take hardcoded borders.
    """

    def __init__(self):
        super().__init__()
        self.create_universe()

    def create_universe(self, timepoint=-1):
        """
        Iterates through all shares and sorts them by their scores.
        This function is where you can define your own strategy.
        Just create child instances of the portfolio class and overwrite this function.
        """

        # Creates the borders for the scoring rules.
        self.rate(lambda stock: stock.data["ROE"][timepoint])
        self.rate(lambda stock: stock.data["Earnings"][timepoint]/stock.data["Revenue"][timepoint])
        self.rate(lambda stock: stock.data["Equity to assets ratio"][timepoint])
        self.rate(lambda stock: stock.data["P/E ratio"][timepoint], positive=False)
        self.rate(lambda stock: stock.data["ROE"][-5], positive=False)
        self.rate(lambda stock: stock.data["Price"][timepoint]/stock.data["Price"][timepoint-2])
        self.rate(lambda stock: stock.data["Price"][timepoint]/stock.data["Price"][timepoint-4])
        self.rate(lambda stock: stock.data["EPS basic"][timepoint]/stock.data["EPS basic"][timepoint-4])



if __name__ == "__main__":
    strat = MyFirstStrategy()
    strat.show_result()
    
#coding=utf-8

import pandas
import glob
import os
import matplotlib.pyplot as plt
import math
import re

import Supporter

from Stock import Stock_Stockpup as SStock
from Stock import Stock_Yahoo as YStock #TODO this is bad! WORKS NOT!

  

class Portfolio(object):
    """
    Creates the optimal portfolio from a given universe of stocks. This is a base class for all kind of freely
    configurable strategies
    """

    def __init__(self, folder = "Stockpup"):
        self.stocklist = []
        self.create_stocklist(folder)

    def create_stocklist(self, folder, maxcounter = 20, **kwargs):
        """Creates the stocklist for this Portfolio by iterating through existing data."""

        counter = 0 #Only for testing reasons, limits the number of used stocks to a given number

        # Creates all shares as Stock-objects
        for share in glob.glob(folder + "/*"):
            try:
                symbol = re.search(r"\\([A-Z]+)", share).group(1)
                self.stocklist.append(SStock(symbol))

                # Only for testing reasons!
                counter += 1
                if counter >= maxcounter:
                    break
      
            except:
                print("Failed on {}".format(share))

    def rate(self, category, border = 0.2, score = 1, positive = True, debug = False):
        """
        This Function is uses to find the best and the worst 20 percent in a given category. This Function is
        used to calculate the score in a more scientific way. In this function, all stocks 
        are rated and a score is given to them.
        """
        borderlist = [category(stock) for stock in self.stocklist if not math.isnan(category(stock))]
        borderlist.sort(reverse = True)
        borders = (borderlist[round(len(borderlist)*border)], borderlist[round(len(borderlist)*(border-1))])
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
    
    def create_correlation_table(self):
        """Creates a table with the correlations of all shares"""
        correlation_table = pandas.DataFrame()
        for x in self.data: 
            # Uses the pearson correlation
            correlation = [Supporter.mypearsonr(self.data[x], self.data[y]) for y in self.data]
            correlation_table[x] = correlation
        correlation_table.index = correlation_table.keys()

        print(correlation_table)
  
    def rebalance(self):
        pass


class MyFirstStrategy(Portfolio):

    def __init__(self):
        super().__init__()

    def create_universe(self, starting_money = 10000, number_of_stocks = 10):
        """
        Iterates through all shares and sorts them by their scores. This function is where you can define your own strategy.
        Just create child instances of the portfolioclass and overwrite this function.
        """
        self.values = {}
        self.equitylist = {}

        # Now the borders for the indivdual scoring system are created
        self.values["ROE"] = self.rate(lambda stock: stock.data["ROE"][-1])
        self.values["EBIT Margin"] = self.rate(lambda stock: stock.data["Earnings"][-1]/stock.data["Revenue"][-1])
        self.values["Equity to assets ratio"] = self.rate(lambda stock: stock.data["Equity to assets ratio"][-1])
        self.values["P/E ratio"] = self.rate(lambda stock: stock.data["P/E ratio"][-1], positive = False)
        self.values["P/E ratio a year ago"] = self.rate(lambda stock: stock.data["ROE"][-5], positive = False)
        self.values["Short Trend"] = self.rate(lambda stock: stock.data["Price"][-1]/stock.data["Price"][-3])
        self.values["Long Trend"] = self.rate(lambda stock: stock.data["Price"][-1]/stock.data["Price"][-5])
        self.values["Change in EPS one year"] = self.rate(lambda stock: stock.data["EPS basic"][-1]/stock.data["EPS basic"][-5])

        self.stocklist.sort(reverse = True)
        capital_per_stock = starting_money / number_of_stocks
        for stock in self.stocklist[:number_of_stocks]:
            self.equitylist[stock.name] = capital_per_stock / stock.data["Price"][-1]
        pass

        self.data = pandas.DataFrame(index = self.stocklist[0].data.index)
        for stock in self.stocklist:
            self.data[stock.name] = stock.data["Price"]


class MyYahooStrategy(Portfolio):

    def __init__(self):
        super().__init__()
        print(self.stocklist)


if __name__ == "__main__":
    #S = Stock("GOOG")
    #Supporter.show_values(S.data, "Equity to assets ratio", "EPS diluted")
    
    #P = MyFirstStrategy()
    #P.create_universe()

    #P.create_correlation_table()

        
    
    Y = MyFirstStrategy()
    Y.create_universe()

    #Y.create_correlation_table() # TODO This works?

    Supporter.show_values(P.data)

    
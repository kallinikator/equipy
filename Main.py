#coding=utf-8

import pandas
import glob
import os
import matplotlib.pyplot as plt
import math
import re

import Supporter
import Stock
  
from Data_access_ystockquote import get_price_data #For backtesting one

class Portfolio(object):
    """
    Creates the optimal portfolio from a given universe of stocks. This is a base class for all kind of freely
    configurable strategies
    """

    def __init__(self, folder = "Stockpup"):
        self.stocklist = []
        self.create_stocklist(folder)
        self.timeline = self.stocklist[0].data.index

        # Is this really needed ? 
        self.portfolio_start_value = 10000
        self.portfolio_value = [10000]

        # This is for Displaying the values of all stocks in the portfolio
        self.data = pandas.DataFrame(index = self.timeline)
        for stock in self.stocklist:
            self.data[stock.name] = stock.data["Price"]


    def create_stocklist(self, folder, maxcounter = 20, **kwargs):
        """Creates the stocklist for this Portfolio by iterating through existing data."""
        counter = 0 #Only for testing reasons, limits the number of used stocks to a given number

        # Creates all shares as Stock-objects
        for share in glob.glob(folder + "/*"):
            try:
                symbol = re.search(r"\\([A-Z]+)", share).group(1)
                self.stocklist.append(Stock.Stock_Stockpup(symbol))

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
    
    def create_correlation_table(self):
        """Creates a table with the correlations of all shares"""
        correlation_table = pandas.DataFrame()
        for x in self.data: 
            # Uses the pearson correlation
            correlation = [Supporter.mypearsonr(self.data[x], self.data[y]) for y in self.data]
            correlation_table[x] = correlation
        correlation_table.index = correlation_table.keys()

        print(correlation_table)


class MyFirstStrategy(Portfolio):

    def __init__(self):
        super().__init__()
        self.run_strategy()

    
    def run_strategy(self, ref="GSPC", *args):
        """
        Tests if your investment idea works. You need to enter at least one reference (more not implemented yet)
        and it you can set a timerange (int, a day each) by the keyword timerange
        """
        # Initializes the reference to the same dates as my data. But it will take every single Day! Oo
        result = pandas.DataFrame(index=self.timeline[4:11])
        reference = get_price_data(ref, self.timeline[0].date().isoformat(), self.timeline[-1].date().isoformat())["Close"]
        add = [] # Ugly as hell!
        for date in self.timeline[4:11]:
            add.append(reference[date.date().isoformat()])
        result["Reference"] = add



        for checkpoint in range(4,len(self.timeline)-1): # Evil hardcoding!
            self.rebalance(checkpoint)
        
        result["Portfolio"] = self.portfolio_value
        Supporter.show_values(result)
 
         
    def rebalance(self, timepoint):
        try:
            total_value = 0
            for stock, number in self.equitylist.items():
                total_value += self.data[stock][timepoint] * number
            self.create_universe(timepoint = timepoint, starting_money = total_value) # The timepoint must be given as a integer, due to idexing
            print("Total value: " + str(total_value))
            self.portfolio_value.append(total_value)
        except:
            self.create_universe(timepoint = timepoint)



    def create_universe(self, starting_money = 10000, number_of_stocks = 10, timepoint = -1): # Starting value hardcode?
        """
        Iterates through all shares and sorts them by their scores. This function is where you can define your own strategy.
        Just create child instances of the portfolioclass and overwrite this function.
        """
        self.equitylist = {}

        # Clears the scores of all stocks to rate them new.
        for stock in self.stocklist:
            stock.score = 0

        # Now the borders for the indivdual scoring system are created
        self.rate(lambda stock: stock.data["ROE"][timepoint])
        self.rate(lambda stock: stock.data["Earnings"][timepoint]/stock.data["Revenue"][timepoint])
        self.rate(lambda stock: stock.data["Equity to assets ratio"][timepoint])
        self.rate(lambda stock: stock.data["P/E ratio"][timepoint], positive = False)
        self.rate(lambda stock: stock.data["ROE"][-5], positive = False)
        self.rate(lambda stock: stock.data["Price"][timepoint]/stock.data["Price"][timepoint-2])
        self.rate(lambda stock: stock.data["Price"][timepoint]/stock.data["Price"][timepoint-4])
        self.rate(lambda stock: stock.data["EPS basic"][timepoint]/stock.data["EPS basic"][timepoint-4])

        # Temporary sorts the stocklist to find out the best stocks. Then splits up the available money between those stocks.
        # The equitylist is emptied everytime you call a new universe.
        capital_per_stock = starting_money / number_of_stocks
        for stock in sorted(self.stocklist, reverse = True)[:number_of_stocks]:
            self.equitylist[stock.name] = capital_per_stock / stock.data["Price"][timepoint] # This is implemented without anything!!!



class MyYahooStrategy(Portfolio):

    def __init__(self):
        super().__init__()
        print(self.stocklist)

    def create_stocklist(self, folder, maxcounter = 20, **kwargs):
        """Creates the stocklist for this Portfolio by iterating through existing data."""
        counter = 0 #Only for testing reasons, limits the number of used stocks to a given number

        # Creates all shares as Stock-objects
        for share in glob.glob(folder + "/*"):
            try:
                symbol = re.search(r"\\([A-Z]+)", share).group(1)
                self.stocklist.append(Stock.Stock_Yahoo(symbol))

                # Only for testing reasons!
                counter += 1
                if counter >= maxcounter:
                    break
      
            except:
                print("Failed on {}".format(share))

    def create_universe(self, starting_money = 10000, number_of_stocks = 10):
        pass



if __name__ == "__main__":
    #S = Stock("GOOG")
    #Supporter.show_values(S.data, "Equity to assets ratio", "EPS diluted")
    
    P = MyFirstStrategy()

    #P.create_correlation_table()

        
    
    #Y = MyYahooStrategy()
    #Y.create_universe()

    ##Y.create_correlation_table() # TODO This works?

    #Supporter.show_values(Y.data)

    
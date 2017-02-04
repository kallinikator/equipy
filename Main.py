#coding=utf-8

import glob
import Stock


class Strategy(object):
    """
    Creates the optimal portfolio from a given universe of stocks. This is a base class for all kind of freely
    configurable strategies
    """
    def __init__(self):
        self.stocklist = []
        self.create_stocklist()

    def __repr__(self):
        return "An instance of a strategy: {}".format(self.stocklist)

    def __len__(self):
        return self.length

    def create_stocklist(self, folder="Stock_Data"):
        """
        Creates the stocklist for this Portfolio by iterating through existing data.
        """

        # counter = 0
        # Only for testing reasons, limits the number of used stocks to a given number
        # Creates all shares as Stock-objects
        for share in glob.glob(folder + "/*.csv"):
            symbol = share.split("\\")[-1].split(".")[0]

            # This is created to filter out stocks with incomplete price data
            stock = Stock.Stock_Stockpup(symbol)
            if stock.complete_pricelist and len(stock) >= 30:
                self.stocklist.append(stock)

            # Only for testing reasons!
            # counter += 1
            # if counter >= 200:
            #     break

        self.length = len(self.stocklist)

    def show_result(self):
        for stock in sorted(self.stocklist, reverse=True):
            print(stock)


class MyFirstStrategy(Strategy):
    """
    This Strategy is implemented as a rating system similar to the ideas of Susan Levermann. In difference to her ideas,
    this strategy is much more diversified (higher amount of stocks) and doesn´t take hardcoded borders.
    """

    def __init__(self):
        super().__init__()

    def create_universe(self, *args, timepoint=0):
        """
        Iterates through all shares and sorts them by their scores.
        This function is where you can define your own strategy.
        Just create child instances of the portfolio class and overwrite this function.
        """
        if "borders" in args:
            function = self.bo_rate
        else:
            function = self.fl_rate

        for stock in self.stocklist:
            stock.score = 0

        # Creates the borders for the scoring rules.
        function(lambda stock: stock.data.loc[stock.data.index[timepoint], "ROE"])
        function(lambda stock: stock.data.loc[stock.data.index[timepoint], "Earnings"] /
                                stock.data.loc[stock.data.index[timepoint], "Revenue"])
        function(lambda stock: stock.data.loc[stock.data.index[timepoint], "Equity to assets ratio"])
        function(lambda stock: stock.data.loc[stock.data.index[timepoint], "P/E ratio"], positive=False)
        function(lambda stock: stock.data.loc[stock.data.index[timepoint+5], "ROE"], positive=False)
        function(lambda stock: stock.data.loc[stock.data.index[timepoint], "Price"] /
                                stock.data.loc[stock.data.index[timepoint+2], "Price"])
        function(lambda stock: stock.data.loc[stock.data.index[timepoint], "Price"] /
                                stock.data.loc[stock.data.index[timepoint+4], "Price"])
        function(lambda stock: stock.data.loc[stock.data.index[timepoint], "EPS basic"] /
                                stock.data.loc[stock.data.index[timepoint+4], "EPS basic"])

    def fl_rate(self, category, positive=True):
        """
        This Function is uses to find the best and the worst 20 percent in a given category. Floating rating.
        """
        resultlist = {}
        for stock in self.stocklist:
            try:
                resultlist[float(category(stock))] = stock
            except:
                pass

        templist = sorted(resultlist.keys(), reverse=True)

        # Sliding scala rating part
        score = 1 / self.length
        for value, stock in resultlist.items():
            if positive:
                stock.score += score - (templist.index(value) * 2 * score) / (len(templist) - 1)
            else:
                stock.score += score - (sorted(templist, reverse=True).index(value) * 2 * score) / \
                                       (len(templist) - 1)

    def bo_rate(self, category, border=0.2, positive=True, debug=False):
        """
        This Function is uses to find the best and the worst 20 percent in a given category.
        """
        resultlist = {}
        for stock in self.stocklist:
            try:
                resultlist[float(category(stock))] = stock
            except:
                pass

        # Creating borders
        templist = sorted(resultlist.keys(), reverse=True)
        borders = (templist[round(len(templist) * border)], templist[round(len(templist) * (1 - border))])

        score = 1
        # Border Rating part
        for rating, stock in resultlist.items():
            if positive:
                if rating > borders[0]:
                    stock.score += score
                if rating <= borders[1]:
                    stock.score -= score
            else:
                if rating > borders[1]:
                    stock.score += score
                if rating <= borders[0]:
                    stock.score -= score
            if debug:  # Allows for further information
                print("Stock:\t{}\nValue:\t{}\nNew rating:\t{}".format(stock.name, category(stock), stock.score))


if __name__ == "__main__":
    strat = MyFirstStrategy()
    strat.create_universe("borders")
    #strat.show_result()

    print(len(strat))

    # TODO Unittest: Implement Scorelist

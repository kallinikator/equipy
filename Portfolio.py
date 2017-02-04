import Main

# TODO Dates!!!

class Portfolio(object):

    def __init__(self, strategy):
        self.strategy = strategy()


    def __repr__(self):
        return "An instance of a portfolio: {}".format(self.positionlist)

    def calculate(self, *args):
        self.positionlist = []
        timepoint = 0
        while timepoint < 30:
            entry = {}
            self.strategy.create_universe(timepoint=timepoint, *args)

            # The place where further args could be used.
            # TODO implement further args

            if "allow_short" in args and not "borders" in args:
                for stock in self.strategy.stocklist:
                    entry[stock.name] = (1 / len(self.strategy.stocklist) + stock.score,
                                             float(stock.data.loc[stock.data.index[timepoint], "Price"]))

            elif "allow_short" in args and "borders" in args:
                good_stocks = []
                for stock in self.strategy.stocklist:
                    if stock.score > 0:
                        good_stocks.append(stock)
                    else:
                        entry[stock.name] = (0, float(stock.data.loc[stock.data.index[timepoint], "Price"]))
                for stock in good_stocks:
                    entry[stock.name] = (1 / len(good_stocks),
                                             float(stock.data.loc[stock.data.index[timepoint], "Price"]))

            self.positionlist.append(entry)
            timepoint += 1

    def create_equal_reference(self):
        """ This creates an equalweight portfolio out of an existing positionlist"""
        for entry in self.positionlist:
            for stock, data in entry.items():
                entry[stock] = (1 / self.strategy.length, data[1])



if __name__ == "__main__":
    portfolio = Portfolio(Main.MyFirstStrategy)
    portfolio.calculate("borders", "allow_short")
    print(portfolio.positionlist)
    portfolio.create_equal_reference()
    print(portfolio.positionlist)

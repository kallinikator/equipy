import Portfolio
import Main
import Supporter


class Backtester(object):

    def __init__(self, portfolio):
        self.portfolio = portfolio(Main.MyFirstStrategy)

    def __repr__(self):
        return "An instance of a Backtester"

    def calculate_portfolio_value(self, *args, money=100000):
        """ This function creates the finals portfolio value if a given portfolio would have been used. """
        if "equalweight" in args:
            self.portfolio.create_equal_reference()
        else:
            self.portfolio.calculate(*args)

        value_of_portfolio = [money]

        # This line unpacks and creates the initial portfolio
        stocks = {stock: (position[0] * money) / position[1] for
                  stock, position in self.portfolio.positionlist[-1].items()}

        # Then, I iterate through the following lines. After updating the money, a new portfolio is created.
        for step in reversed(self.portfolio.positionlist[:-1]):
            #print(len(stocks),len(step), self.portfolio.strategy.length)
            assert len(stocks) == len(step) == self.portfolio.strategy.length
            money = 0
            for stock, position in step.items():
                money += stocks[stock] * position[1]

            value_of_portfolio.append(money)
            stocks = {}
            for stock, position in step.items():
                stocks[stock] = (position[0] * money) / position[1]

        print("Portfolio Values created!")
        return value_of_portfolio


if __name__ == "__main__":
    import pandas

    backtest = Backtester(Portfolio.Portfolio)
    result = pandas.DataFrame()
    result["ba"] = backtest.calculate_portfolio_value("borders", "allow_short")
    result["fa"] = backtest.calculate_portfolio_value("floating", "allow_short")
    result["n"] = backtest.calculate_portfolio_value("equalweight")
    print(result)

    Supporter.show_values(result)

# TODO write a proper documentation
# TODO Other flags
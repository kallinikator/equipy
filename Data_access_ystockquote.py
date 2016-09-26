import ystockquote
import Supporter
import pandas


@Supporter.myLogger
def get_price_data(stock: str, *timepoints: str) -> pandas.DataFrame:
    """
    Gets Price Data from yahoo finance. 
    Enter a starting point and an endpoint as args after entering the symbol of a stock or an index.  

    The´result will look like this:

    2013-01-03: {Adj Close: 8.692095,
                 Close: 9.07,
                 High: 9.15,
                 Low: 8.95,
                 Open: 8.97,
                 Volume: 22302800},
    2013-01-04: {Adj Close: 8.874179,
                 Close: 9.26,
                 High: 9.28,
                 Low: 9.10,
                 Open: 9.11,
                 Volume: 18345300},
    2013-01-07: {Adj Close: 8.720846,
                 Close: 9.10,
                 High: 9.29,
                 Low: 9.10,
                 Open: 9.28,
                 Volume: 21785000},
    2013-01-08: {Adj Close: 8.720846,
                 Close: 9.10,
                 High: 9.19,
                 Low: 9.08,
                 Open: 9.16,
                 Volume: 34078700}
    """

    try:
        return pandas.DataFrame(ystockquote.get_historical_prices(stock, *timepoints), dtype='float').T
    except:
        print("Something went wrong!")


@Supporter.myLogger
def get_fundamental_data(stock: str) -> dict:
    """
    Gets fundamental Data from yahoo finance. Some fundamentals and a lot af real-live prices.
    Enter a starting point and an endpoint as args after entering the symbol of a stock or an index. 
    The result will look like this:

      avg_daily_volume: 17735800,
      book_value: 9.33,
      change: -0.13,
      dividend_per_share: 0.12,
      dividend_yield: 1.23,
      earnings_per_share: -0.44,
      ebitda: 2.63B,
      fifty_day_moving_avg: 10.28,
      fifty_two_week_high: 11.50,
      fifty_two_week_low: 6.14,
      market_cap: 12.35B,
      price: 9.39,
      price_book_ratio: 1.02,
      price_earnings_growth_ratio: 2.50,
      price_earnings_ratio: N/A,
      price_sales_ratio: 0.59,
      short_ratio: 8.07,
      stock_exchange: "NYQ",
      two_hundred_day_moving_avg: 9.91,
      volume: 15300774},  

    """
    try:
        return ystockquote.get_all(stock)
    except:
        print("Something went wrong!")

    

if __name__ == "__main__":
    result = get_price_data("MYR", "2013-01-03", "2013-01-08", "2013-02-08")
    #print(result)
    #result = get_fundamental_data("MYR")
    #print(result)




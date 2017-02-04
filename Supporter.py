import logging
import time
import pandas

import matplotlib.pyplot as plt


def myLogger(func):
    """Will create a logfile which will track all taken args and kwargs and infos of modules"""
    logging.basicConfig(filename="{}.log".format(func.__name__), level=logging.INFO)
    
    def wrapper(*args,**kwargs):
        logging.info("Args: {}, Kwargs: {}".format(args, kwargs))
        return func(*args,**kwargs)
    return wrapper


def portfolio_analyser(func):
    """
    This Function is used to explain changes in portfoliovalues by tracking all kind of input.
    Furthermore, this function is used to calculate the most popular risk measurements.
    """
    def wrapper(*args, **kwargs):
        with open("outputfile.txt", "w") as file:
            for arg in args:
                file.write("{}\n".format(str(arg)))
            for kw, arg in kwargs:
                file.write("{} : {}\n".format(str(kw), str(arg)))
        return func(*args, **kwargs)

    return wrapper


def myTimer(func):
    """Is used to measure the time needed. Useful for performance testing"""
    def wrapper(*args,**kwargs):
        start = time.time()
        func(*args,**kwargs)
        end = time.time()
        print("The function {} needed {} seconds!".format(func.__name__, end - start))
    return wrapper


def show_values(values):
    """Shows a passed Dataframe. You can specify which rows to show by passing args"""  
    plt.style.use("ggplot")
    plt.title("Result")
    values.plot()
    plt.show()


def mypearsonr(x, y):
    """Calculates Pearson without scipy. Creds go to stackoverflow."""
    assert len(x) == len(y) != 0
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(len(x)):
        xdiff = x[idx] - x.mean()
        ydiff = y[idx] - y.mean()
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff
    return diffprod / (xdiff2 * ydiff2) ** 0.5


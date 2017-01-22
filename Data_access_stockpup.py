import requests
import bs4
import os
import re


def get_fundamentals(*args, **kwargs):
    base_url = "http://www.stockpup.com/data/"

    session = requests.Session()

    site = bs4.BeautifulSoup(session.get(base_url).content, "lxml")

    if not os.path.exists("Stock_Data"):
        os.mkdir("Stock_Data")

    for link in site.findAll(name="a", text="CSV"):
        filename = os.path.join("Stock_Data", re.match(r"/data/([A-Z]+)", link["href"]).group(1) + ".csv")
        with open(filename, "w") as file:
            csv = session.get("http://www.stockpup.com" + link["href"])
            file.write(csv.text)
            print("write {}".format(filename))


if __name__ == "__main__":
    get_fundamentals()

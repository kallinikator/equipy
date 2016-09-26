import requests
import bs4
import os
import re
import sys


URL = "http://www.stockpup.com/"
FILENAME = re.compile(r"([A-Za-z_]+).csv")
PATH = os.getcwd()

#@Supporter.myLogger
def crawl_data(PATH):
    
    if not os.path.exists("Stockpup"):
        os.makedirs("Stockpup")
    PATH = os.path.join(PATH, "Stockpup")
    print(PATH)
        
    with requests.Session() as crawlsession:
        
        page = crawlsession.get(URL + r"data/")
        tree = bs4.BeautifulSoup(page.content, "lxml")
     
        for link in tree.findAll("a", href = True):
            link = link.get("href")
            
            if ".csv" in link:
                Filename = re.search(FILENAME, link).group(1)    
                filepath = os.path.join(PATH, Filename)
                if not os.path.exists(filepath):
                    os.makedirs(filepath)     
                csv = crawlsession.get(URL + link)
                with open(os.path.join(filepath, Filename) + r".csv", "w") as myfile:
                    myfile.write(csv.content.decode("utf-8"))
                print(link + " downloaded")

if __name__ == "__main__":
    crawl_data(PATH)
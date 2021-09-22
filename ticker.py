#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import requests, json, argparse, argcomplete
from prettytable import PrettyTable
from stockset import StockSet
from os import listdir, system, name
from time import sleep

# Constants
API_ENDPOINT = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com"
FIELDS = ','.join(map(str, ["symbol", "marketState", "displayName", "regularMarketPrice", "regularMarketChange", "regularMarketChangePercent", "preMarketPrice",
"preMarketChange", "preMarketChangePercent", "postMarketPrice", "postMarketChange", "postMarketChangePercent"]))
STOCKS_SET_DIR = "~/VSCode/StockTicker/stocks"

def main():
    args = getArgs()
    stockSets = []

    # Get all stock sets created
    for stockFile in listdir(STOCKS_SET_DIR):
        newStockSet = getStockSetFromFile(STOCKS_SET_DIR + stockFile)
        if newStockSet == []: # Response if we fail to read the stock set
            continue
        stockSets.append(newStockSet)

    if args.updateTime == 0: # Only display stocks once
        updateAndDisplayStocks(stockSets, False, args.updateTime)
    else: # Display stocks forever
        while True:
            updateAndDisplayStocks(stockSets, args.clearScreen, args.updateTime)
        

def updateAndDisplayStocks(stockSets: list, clearScreen: bool = False, updateTime: int = 0):
    for currStockSet in stockSets:
        currStockSet.updateAllStocks(getDataFromMarket(currStockSet.getSymbols()))
    if clearScreen: system('cls' if name=='nt' else 'clear')
    for currStockSet in stockSets:
        table = PrettyTable(currStockSet.getTableHeaders())

        for stock in currStockSet.getAllStockArrays():
            table.add_row(stock)
        table.sortby = currStockSet.getTableSortByCol()

        print(currStockSet.getName(True))
        print(table)
    sleep(updateTime)

def getStockSetFromFile(filename: str):
    try:
        file = open(filename, "r")
        jsonStocksArray = json.loads(file.read())
        file.close()
    except:
        print("Error reading file:", filename)
        return []

    newStockSet = StockSet(jsonStocksArray["name"], jsonStocksArray["displayShares"])
    for jsonStock in jsonStocksArray["stocks"]:
        if (newStockSet.getDisplayShares()):
            newStockSet.addStock(jsonStock["symbol"], jsonStock["shareCount"], jsonStock["shareOriginalValue"])
        else:
            newStockSet.addStock(jsonStock["symbol"])
    return newStockSet

# Returns an array with all the results for all the given symbols
def getDataFromMarket(symbols: list):
    response = requests.get(
        url=API_ENDPOINT, 
        params={
            "fields": FIELDS,
            "symbols": ','.join(map(str, symbols))
        }
    )

    if (response.status_code == 200):
        return response.json()["quoteResponse"]["result"]
    else:
        return [] # Return an empty array to signal an error occured

    print (response.json()["quoteResponse"]["result"])

def getArgs():
    parser = argparse.ArgumentParser(prog=__file__)

    parser.add_argument('-u','--update-time', default=10, type=int, dest='updateTime', help="Time in between stock updates. 10 is default. 0 will only run it once")
    parser.add_argument('-c','--clear', default=True, type=bool, dest='clearScreen', help="Clear the screen on each stock update. Default is true. If update-time is 0 will always be false")
    # parser.add_argument('-s', '--sort-by', nargs='?', choices=['name', 'symbol', 'equity', 'shares', 'msrtest', 'railnet'], default=configs["defaultApp"], help="Application to build")
    argcomplete.autocomplete(parser)

    return parser.parse_args()

if __name__== "__main__":
  main()

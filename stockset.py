from stock import Stock
import locale

# class COLORS:
#     BOLD = "\033[1m"
#     END_COLOR = "\033[0m"
#     GREEN = "\033[92m"
#     YELLOW = "\033[93m"
#     RED = "\033[91m"
#     WHITE = "\033[97m"


#     def setColor(color: str, target: str):
#         return color + target + self.END_COLOR

class StockSet:
    BOLD = "\033[1m"
    END_COLOR = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"

    def setColor(self, color: str, target: str):
        return color + target + self.END_COLOR

    def __init__(self, name: str, displayShares: bool = False):
        self.name = name
        self.displayShares = displayShares
        self.stocksDict = {}
        locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.getName() + ": " + str(self.getStocks())

    def getName(self, asBold: bool = False):
        if asBold:
            return self.setColor(self.BOLD, self.name)
        return self.name

    def getDisplayShares(self):
        return self.displayShares

    def getStocks(self):
        return self.stocksDict

    def addStock(self, newStock: Stock):
        self.stocksDict[newStock.getSymbol()] = newStock

    def addStock(self, symbol: str, shareCount: int = 0, shareOriginalValue: float = 0):
        self.stocksDict[symbol] = Stock(symbol,shareCount, shareOriginalValue)

    def updateStock(self, symbol: str, displayName: str, currentPrice: float, changeAmount: float, changePercentage: float):
        if symbol not in self.stocksDict:
            return False
        self.stocksDict[symbol].setCurrentMarketData(displayName, currentPrice, changeAmount, changePercentage)
        return True

    def updateAllStocks(self, updatedStockList: list):
        for currStockObject in updatedStockList:
            try:
                fieldPrefix = currStockObject["marketState"].lower()
                changeAmount = currStockObject[fieldPrefix + "MarketChange"] if fieldPrefix == "regular" else currStockObject[fieldPrefix + "MarketChange"] + currStockObject["regular" + "MarketChange"]
                changePercent = currStockObject[fieldPrefix + "MarketChangePercent"] if fieldPrefix == "regular" else currStockObject[fieldPrefix + "MarketChangePercent"] + currStockObject["regular" + "MarketChangePercent"]
                self.updateStock(
                    symbol=currStockObject["symbol"], 
                    displayName=currStockObject["displayName"], 
                    currentPrice=currStockObject[fieldPrefix + "MarketPrice"],
                    changeAmount=changeAmount,
                    changePercentage=changePercent
                )
            except:
                print ("error")


    def getSymbols(self):
        return self.stocksDict.keys()

    def getSingleStockArray(self, stock: Stock) -> list:
        displayName = stock.getDisplayName()
        symbol = stock.getSymbol()
        currPrice = self.moneyToString(stock.getCurrentPrice())

        currColor = self.getStockColor(stock.getLastestChangeAmount())
        currChangeAmount = self.setColor(currColor, self.moneyToString(stock.getLastestChangeAmount()))
        currChangePercentage = self.setColor(currColor, self.percentToString(stock.getLatestChangePercentage()))

        if (self.getDisplayShares()):
            totalColor = self.getStockColor(stock.getTotalChangeAmount())
            shareCount = self.setColor(totalColor, str(stock.getShareCount()))
            totalChangeAmount = self.setColor(totalColor, self.moneyToString(stock.getTotalChangeAmount()))
            totalChangePercent = self.setColor(totalColor, self.percentToString(stock.getTotalChangePercentage()))
            equity = self.setColor(totalColor, self.moneyToString(stock.getCurrentEquity()))

            if totalColor == currColor:
                displayName = self.setColor(totalColor, displayName)
                symbol = self.setColor(totalColor, symbol)
                currPrice = self.setColor(totalColor, currPrice)
        else:
            displayName = self.setColor(currColor, displayName)
            symbol = self.setColor(currColor, symbol)
            currPrice = self.setColor(currColor, currPrice)

        stockArray = [
            displayName,
            symbol,
            currPrice,
            currChangeAmount,
            currChangePercentage
        ]
        if (self.getDisplayShares()):
            stockArray += [
                shareCount,
                totalChangeAmount,
                totalChangePercent,
                equity
            ]

        return stockArray
    
    def getAllStockArrays(self) -> list:
        tableArray = []
        for stock in self.stocksDict:
            tableArray.append(self.getSingleStockArray(self.stocksDict[stock]))

        return tableArray

    def getTableHeaders(self) -> list:
        headers = ["Name", "Symbol", "Price", "Daily change", "Daily change %"]
        if (self.getDisplayShares()):
            headers += ["Shares", "Equity change", "Equity change %", "Equity"]
        return headers

    def getTableSortByCol(self):
        return "Name"

    def moneyToString(self, amount):
        return locale.currency(amount, grouping=True)

    def percentToString(self, percent):
        return str(round(percent, 2)) + "%"

    def getStockColor(self, val):
        if val > 0:
            return self.GREEN
        elif val < 0:
            return self.RED
        else: # val == 0
            return self.YELLOW
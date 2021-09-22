

class Stock:

    def __init__(self, symbol: str, shareCount: int = 0, shareOriginalValue: float = 0):
        self.symbol = symbol
        self.shareCount = shareCount
        self.shareOriginalValue = shareOriginalValue

        self.displayName = "Unknown"
        self.currentPrice = 0
        self.dailyChangeAmount = 0
        self.dailyChangePercentage = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.getSymbol()

    def setCurrentMarketData(self, displayName: str, currentPrice: float, changeAmount: float, changePercentage: float):
        self.displayName = displayName
        self.currentPrice = currentPrice
        self.dailyChangeAmount = changeAmount
        self.dailyChangePercentage = changePercentage

    def getSymbol(self):
        return self.symbol

    def getShareCount(self):
        return self.shareCount

    def getShareOriginalValue(self):
        return self.shareOriginalValue

    def getDisplayName(self):
        return self.displayName

    def getCurrentPrice(self):
        return self.currentPrice

    def getLastestChangeAmount(self):
        return self.dailyChangeAmount

    def getLatestChangePercentage(self):
        return self.dailyChangePercentage

    def getCurrentEquity(self):
        return self.getCurrentPrice() * self.getShareCount()

    def getTotalChangeAmount(self):
        return self.getCurrentEquity() - (self.getShareCount() * self.getShareOriginalValue())

    def getTotalChangePercentage(self):
        if self.getCurrentPrice() == self.getShareOriginalValue():
            return 0
        try:
            return (abs(self.getCurrentPrice() - self.getShareOriginalValue()) / self.getShareOriginalValue()) * 100.0
        except ZeroDivisionError:
            return 100
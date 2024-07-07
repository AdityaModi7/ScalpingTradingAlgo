from AlgorithmImports import *

class ImprovedStrategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        self.symbols = ["AAPL", "GOOGL", "AMZN", "MSFT"]
        self.lookback_momentum = 20  # Lookback period for momentum calculation
        self.lookback_volatility = 30  # Lookback period for volatility calculation

        self.momentum = {}
        self.volatility = {}
        self.invested = {}

        for symbol in self.symbols:
            self.AddEquity(symbol, Resolution.Daily)
            self.momentum[symbol] = self.MOMP(symbol, self.lookback_momentum, Resolution.Daily)
            self.volatility[symbol] = self.STD(symbol, self.lookback_volatility, Resolution.Daily)
            self.invested[symbol] = False

    def OnData(self, data):
        for symbol in self.symbols:
            if not all(indicator.IsReady for indicator in [self.momentum[symbol], self.volatility[symbol]]):
                return

            momentum_value = self.momentum[symbol].Current.Value
            volatility_value = self.volatility[symbol].Current.Value

            # Buy if the stock exhibits positive momentum and higher volatility and not already invested
            if momentum_value > 0 and volatility_value > 0 and not self.invested[symbol]:
                self.SetHoldings(symbol, 1 / len(self.symbols))  # Equally weight each stock
                self.invested[symbol] = True
                self.Debug(f"Buy Signal (Momentum & Volatility strategy) for {symbol}")

            # Sell if the momentum or volatility turns negative and the stock is invested
            elif (momentum_value <= 0 or volatility_value <= 0) and self.invested[symbol]:
                self.Liquidate(symbol)
                self.invested[symbol] = False
                self.Debug(f"Sell Signal (Momentum & Volatility strategy) for {symbol}")

    def OnEndOfDay(self):
        for symbol in self.symbols:
            self.Debug(f"Momentum ({symbol}): {self.momentum[symbol].Current.Value}, Volatility ({symbol}): {self.volatility[symbol].Current.Value}")

import pandas as pd
import ValueAtRisk as Risk
import yfinance as yf

# Define constants
holding_period = 10
t_period = 250

training_start = '2012-12-01'
training_end = '2018-01-01'

testing_start = '2017-12-01'
testing_end = '2019-01-01'

# Define output CSV headers
headers = ['Ticker',
           'VaR@99.5%', 'VaR@99.0%', 'VaR@98.5%', 'VaR@98.0%', 'VaR@97.5%', 'ES',
           'Excep@99.5%', 'Excep@99.0%', 'Excep@98.5%', 'Excep@98.0%', 'Excep@97.5%', 'Excep@ES%']

# Define tickers lists
tickers_technology = ['MSFT','AAPL','V','MA','CSCO','INTC','ADBE','ORCL','SAP.DE','PYPL',
                      'IBM','CRM','AVGO','ACN','TXN','NVDA','ASML.AS','ADP','QCOM','INTU']
tickers_banks = ['JPM','BAC','WFC','HSBA.L','C','RY.TO','TD.TO','CBA.AX','USB','SAN.MC',
                 'BNS.TO','WBC.AX','8306.T','LLOY.L','BNP.PA','ANZ.AX','INGA.AS','BMO.TO','NAB.AX','8316.T']


def download_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_prices = stock_data['Adj Close']
    stock_returns = stock_prices.pct_change(holding_period).dropna()
    return stock_returns


def process_ticker(ticker):
    # Download training and backtesting data
    training_data = download_data(ticker, training_start, training_end)
    testing_data = download_data(ticker, testing_start, testing_end).tail(t_period)

    # Calculate VaR at all 5 confidence levels
    var_975 = Risk.value_at_risk(training_data, 0.025)
    var_980 = Risk.value_at_risk(training_data, 0.02)
    var_985 = Risk.value_at_risk(training_data, 0.015)
    var_990 = Risk.value_at_risk(training_data, 0.01)
    var_995 = Risk.value_at_risk(training_data, 0.005)

    # Calculate Expected Shortfall
    es = Risk.expected_shortfall(training_data, 0.025)

    # Backtesting
    exceptions_975 = Risk.backtesting(testing_data, var_975)
    exceptions_980 = Risk.backtesting(testing_data, var_980)
    exceptions_985 = Risk.backtesting(testing_data, var_985)
    exceptions_990 = Risk.backtesting(testing_data, var_990)
    exceptions_995 = Risk.backtesting(testing_data, var_995)
    exceptions_es = Risk.backtesting(testing_data, es)

    result = [ticker, var_995, var_990, var_985, var_980, var_975, es,
              exceptions_995, exceptions_990, exceptions_985, exceptions_980, exceptions_975, exceptions_es]

    return result


df = pd.DataFrame(columns=headers)
tickers = tickers_technology + tickers_banks
for ticker in tickers:
    print(ticker)
    result = process_ticker(ticker)
    df = df.append(pd.Series(result, index=df.columns), ignore_index=True)

df.to_csv('output.csv')
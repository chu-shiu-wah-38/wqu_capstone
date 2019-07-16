import pandas as pd


# Define variables
max_exceptions_allowed = [2,4,6,8,10]


def value_at_risk(returns, confidence_level):
    """
    Compute the Value-at-Risk metric of returns at confidence_level
    :param returns: DataFrame
    :param confidence_level: float
    :return: float
    """

    # Calculate the highest return in the lowest quantile (based on confidence level)
    var = returns.quantile(q=confidence_level, interpolation="higher")
    return var


def expected_shortfall(returns, confidence_level):
    """
    Compute the Value-at-Risk metric of returns at confidence_level
    :param returns: DataFrame
    :param confidence_level: float
    :return: float
    """

    # Calculate the VaR of the returns
    var = value_at_risk(returns, confidence_level)
    # Find all returns in the worst quantitle
    worst_returns = returns[returns.lt(var)]
    # Calculate mean of all the worst returns
    es = worst_returns.mean()

    return es


def backtesting(returns, threshold):
    """
    Calculate the number of exceptions in returns that
    :param returns: DataFrame
    :param threshold: float
    :return: int
    """

    exceptions = list(filter(lambda x: x < threshold, returns))
    print(exceptions)
    return len(exceptions)
from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    opm_cross_check,
    return_on_equity
)

print("Net Profit Margin")
print(net_profit_margin(500, 1000))

print("\nOperating Profit Margin")
opm = operating_profit_margin(300, 1000)
print(opm)

print("\nCross Check")
print(opm_cross_check(opm, 30))
print(opm_cross_check(opm, 28))
print(opm_cross_check(opm, 25))
print(opm_cross_check(None, 30))
from src.analytics.ratios import return_on_equity

print("\nReturn On Equity")

print(return_on_equity(500, 1000, 500))
print(return_on_equity(250, 500, 500))
print(return_on_equity(100, 0, 0))
print(return_on_equity(100, 100, -200))


from src.analytics.ratios import (
    return_on_capital_employed,
    roce_benchmark
)

print("\nROCE")

print(return_on_capital_employed(
    500,
    50,
    1000,
    500,
    500
))

print(return_on_capital_employed(
    100,
    20,
    0,
    0,
    0
))

print(return_on_capital_employed(
    200,
    30,
    -500,
    100,
    100
))

print()

print(roce_benchmark(22, "Industrials"))
print(roce_benchmark(18, "Financials"))

from src.analytics.ratios import return_on_assets

print("\nReturn On Assets")

print(return_on_assets(500, 2000))
print(return_on_assets(100, 1000))
print(return_on_assets(100, 0))
print(return_on_assets(100, -500))
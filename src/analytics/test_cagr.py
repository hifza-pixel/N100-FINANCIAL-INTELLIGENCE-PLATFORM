from src.analytics.cagr import calculate_cagr,revenue_cagr,pat_cagr,eps_cagr

print(calculate_cagr(100, 200, 5))
print(calculate_cagr(100, -50, 5))
print(calculate_cagr(-100, 50, 5))
print(calculate_cagr(-100, -50, 5))
print(calculate_cagr(0, 100, 5))
print(calculate_cagr(100, 200, 0))



history = {

    2014:100,
    2015:120,
    2016:140,
    2017:170,
    2018:200,
    2019:230,
    2020:260,
    2021:300,
    2022:350,
    2023:420,
    2024:500

}

print()

print("Revenue CAGR")

result = revenue_cagr(history)

for k, v in result.items():
    print(k, ":", v)


history = {

    2014:100,
    2015:120,
    2016:140,
    2017:170,
    2018:200,
    2019:230,
    2020:260,
    2021:300,
    2022:350,
    2023:420,
    2024:500

}

print("\nRevenue")
print(revenue_cagr(history))

print("\nPAT")
print(pat_cagr(history))

print("\nEPS")
print(eps_cagr(history))
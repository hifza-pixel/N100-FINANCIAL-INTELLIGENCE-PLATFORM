from src.analytics.cashflow_kpis import free_cash_flow, cfo_quality_score,capex_intensity,fcf_conversion_rate,capital_allocation_pattern

print("Free Cash Flow")

print(free_cash_flow(500, -120))
print(free_cash_flow(300, -500))
print(free_cash_flow(-100, -200))

print("\nCFO Quality Score")

cfo = [120, 150, 170, 180, 200]
pat = [100, 120, 150, 160, 180]

score, label = cfo_quality_score(cfo, pat)

print(score)
print(label)

print()

cfo = [60, 70, 80, 90, 100]
pat = [120, 130, 140, 150, 160]

score, label = cfo_quality_score(cfo, pat)

print(score)
print(label)

print()

cfo = [20, 25, 30, 35, 40]
pat = [100, 100, 100, 100, 100]

score, label = cfo_quality_score(cfo, pat)

print(score)
print(label)
print("\nCapEx Intensity")

print(capex_intensity(-20,1000))
print(capex_intensity(-50,1000))
print(capex_intensity(-150,1000))
print(capex_intensity(-100,0))
print("\nFCF Conversion")

print(fcf_conversion_rate(350,500))
print(fcf_conversion_rate(100,250))
print(fcf_conversion_rate(-150,400))
print(fcf_conversion_rate(100,0))


print("\nCapital Allocation\n")

print(capital_allocation_pattern(500, -200, -150, 1.3))
print(capital_allocation_pattern(500, -200, -150, 0.8))
print(capital_allocation_pattern(500, 200, -100))
print(capital_allocation_pattern(-100, 50, 70))
print(capital_allocation_pattern(-100, -50, 120))
print(capital_allocation_pattern(200, 100, 150))
print(capital_allocation_pattern(-100, -50, -20))
print(capital_allocation_pattern(100, -50, 80))
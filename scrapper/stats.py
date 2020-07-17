import pandas as pd

rates_data = pd.read_csv("EUR_GBP Historical Data.csv")

mx = max([rates_data.at[i, "Price"] for i in range(len(rates_data) - int(80*len(rates_data) / 100), -1, -1)])
mn = min([rates_data.at[i, "Price"] for i in range(len(rates_data) - int(80*len(rates_data) / 100), -1, -1)])
print(mx, mn)
rmse = 0.007848300039768219
print(rmse/(mx-mn))

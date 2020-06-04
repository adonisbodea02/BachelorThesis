import pandas as pd

rates_data = pd.read_csv("GBP_USD Historical Data.csv")

mean = 0
for i in range(len(rates_data)):
    mean += rates_data.at[i, "Price"]
print(len(rates_data))
mean = mean / len(rates_data)
print(mean)
print(0.0076088509522378445/mean)

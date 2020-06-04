import pandas as pd

inflationEU_data = pd.read_csv("Inflation Rate UK.csv")
rates_data = pd.read_csv("EUR_GBP Historical Data.csv")

# new_inflationEU_data = []
# for i in range(len(inflationEU_data)):
#     date = inflationEU_data.at[i, "Date"]
#     date = date.strip()
#     date = date.split(' ')
#     if date[0] == "Jan." or date[0] == "January":
#         date[0] = "Jan"
#     elif date[0] == "Feb." or date[0] == "February":
#         date[0] = "Feb"
#     elif date[0] == "Mar." or date[0] == "March":
#         date[0] = "Mar"
#     elif date[0] == "Apr." or date[0] == "April":
#         date[0] = "Apr"
#     elif date[0] == "May." or date[0] == "May":
#         date[0] = "May"
#     elif date[0] == "Jun." or date[0] == "June":
#         date[0] = "Jun"
#     elif date[0] == "Jan." or date[0] == "January":
#         date[0] = "Jan"
#     elif date[0] == "Jul." or date[0] == "July":
#         date[0] = "Jul"
#     elif date[0] == "Aug." or date[0] == "August":
#         date[0] = "Aug"
#     elif date[0] == "Sept." or date[0] == "September":
#         date[0] = "Sep"
#     elif date[0] == "Oct." or date[0] == "October":
#         date[0] = "Oct"
#     elif date[0] == "Nov." or date[0] == "November":
#         date[0] = "Nov"
#     elif date[0] == "Dec." or date[0] == "December":
#         date[0] = "Dec"
#     if date[1] == '1,' or date[1] == '2,' or date[1] == '3,' or date[1] == '4,' or date[1] == '5,' or date[1] == '6,' or date[1] == '7,' or date[1] == '8,' or date[1] == '9,':
#         date[1] = '0' + date[1]
#     new_date = date[0] + ' ' + date[1] + ' ' + date[2]
#     new_inflationEU_data.append([new_date, inflationEU_data.at[i, "Price"]])

new_inflationEU_data = []
for i in range(len(inflationEU_data)):
    inflation_date = inflationEU_data.at[i, "Date"]
    inflation_date = inflation_date.strip()
    inflation_date = inflation_date.split(' ')

    for j in range(len(rates_data)):
        rate_date = rates_data.at[j, "Date"]
        rate_date = rate_date.strip()
        rate_date = rate_date.split(' ')

        if inflation_date[0] == rate_date[0] and inflation_date[2] == rate_date[2]:
            new_date = rate_date[0] + ' ' + rate_date[1] + ' ' + rate_date[2]
            new_inflationEU_data.append([new_date, inflationEU_data.at[i, "Price"]])

for i in new_inflationEU_data:
    print(i)

inflationEU_rates = pd.DataFrame(new_inflationEU_data, columns=['Date', 'Price'])
inflationEU_rates.to_csv('Inflation Rate UK.csv', index=False)

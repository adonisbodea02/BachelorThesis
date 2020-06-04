import pandas as pd


# gold_data = pd.read_csv("Gold Price Historical Data.csv")
# rates_data = pd.read_csv("EUR_GBP Historical Data.csv")
# oil_data = pd.read_csv("Oil Brent Spot Price.csv")
inflationEU_data = pd.read_csv("Inflation Rate EU.csv")

# gold_data_list = []
# rates_data_list = []
# oil_data_list = []
# for i in range(len(gold_data)):
#     gold_data_list.append(gold_data.at[i, "Date"].strip())
#
# for i in range(len(rates_data)):
#     rates_data_list.append(rates_data.at[i, "Date"].strip())
#
# for i in range(len(oil_data)):
#     oil_data_list.append(oil_data.at[i, "Date"].strip())
#
# j = 0
# for i in oil_data_list:
#     if i not in rates_data_list:
#         print(i)
# #
# print('split')
# # #
# j = 0
# for i in rates_data_list:
#     if i not in oil_data_list:
#         print(i)
#         j += 1
# print(j)
# with open("price.txt") as f:
#     while True:
#         line1 = f.readline()
#         if not line1:
#             break
#         line2 = f.readline()
#         data.append([line1, line2])

# new_data = []
# for i in range(len(gold_data)):
#     date = gold_data.at[i, "Date"]
#     date = date.strip()
#     date = date.split(' ')
#     if date[1] == '1,' or date[1] == '2,' or date[1] == '3,' or date[1] == '4,' or date[1] == '5,' or date[1] == '6,' or date[1] == '7,' or date[1] == '8,' or date[1] == '9,':
#         date[1] = '0' + date[1]
#     new_date = date[0] + ' ' + date[1] + ' ' + date[2]
#     print(new_date)
#     new_data.append([new_date, gold_data.at[i, "Price"]])

# new_oil_data = []
# for i in range(len(oil_data)):
#     date = oil_data.at[i, "Date"]
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
#     print(new_date)
#     new_oil_data.append([new_date, oil_data.at[i, "Price"]])
# #
# # for i in new_data:
# #     print(i)
# #
# gold_prices = pd.DataFrame(new_data, columns=['Date', 'Price'])
# gold_prices.to_csv('Gold Price Historical Data.csv', index=False)

# oil_prices = pd.DataFrame(new_oil_data, columns=['Date', 'Price'])
# oil_prices.to_csv('Oil Brent Spot Price.csv', index=False)

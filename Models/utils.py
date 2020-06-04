from datetime import timedelta, date, datetime

import requests


def get_weekday_n_days_ago(start_date, n):
    """
    Function which for a given date computes the weekday which was n weekdays ago
    :param start_date: Date, the date from where to start counting
    :param n: Integer, the number of weekdays to look back
    :return: Date, the weekday which was n weekdays ago
    Constraint: n must be less than 30
    """
    prev_days = [start_date - timedelta(days=i) for i in range(1, 40)]
    prev_days = [d for d in prev_days if d.weekday() < 5]
    for d in prev_days:
        if d.month == 5 and d.day == 1:
            prev_days.remove(d)
    return prev_days[n-1]


print(get_weekday_n_days_ago(datetime.strptime('2020-05-31', '%Y-%m-%d').date(), 15))
print(get_weekday_n_days_ago(date.today() + timedelta(days=1), 15))


def get_data(end_date, n, local, foreign):
    """
    Function which for a given date retrieves the last n observations of the specified exchange rate
    :param end_date: Date, the date of the last observation
    :param n: Integer, the number of observations needed
    :param local: String, the local currency
    :param foreign: String, the foreign currency
    :return:
    """
    URL = "https://api.exchangeratesapi.io/history"
    PARAMS = {'start_at': str(get_weekday_n_days_ago(end_date, n)),
              'end_at': str(end_date),
              'symbols': foreign,
              'base': local}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    input_data = []
    for day in data['rates']:
        input_data.append([datetime.strptime(day, '%Y-%m-%d').date(),
                           float("{:.8f}".format(data['rates'][day][foreign]))])
    input_data.sort(key=lambda x: x[0])
    return input_data[-n:]


# d = get_data(datetime.strptime('2020-05-29', '%Y-%m-%d').date() - timedelta(days=1), 15, "EUR", "GBP")
# for j in d:
#     print(j)

d = get_data(date.today(), 15, "EUR", "GBP")
for j in d:
    print(j)

import datetime
import requests


def get_weekday_n_days_ago(n):
    today = datetime.date.today()
    prev_days = [today - datetime.timedelta(days=i) for i in range(30)]
    prev_days = [d for d in prev_days if d.weekday() < 5]
    for d in prev_days:
        if d.month == 5 and d.day == 1:
            prev_days.remove(d)
    return prev_days[n-1]

# https://api.exchangeratesapi.io/history?start_at=2018-01-01&end_at=2018-09-01&symbols=ILS,JPY


d = datetime.datetime.strptime('2020-05-08', '%Y-%m-%d').date()
print(d)
URL = "https://api.exchangeratesapi.io/history"
PARAMS = {'start_at': str(get_weekday_n_days_ago(15)),
          'end_at': str(datetime.date.today()),
          'symbols': 'GBP'}
r = requests.get(url=URL, params=PARAMS)
data = r.json()
input_model = []
for day in data['rates']:
    input_model.append([datetime.datetime.strptime(day, '%Y-%m-%d').date(),
                        float("{:.8f}".format(data['rates'][day]['GBP']))])

input_model.sort(key=lambda x: x[0])
for i in input_model:
    print(i)

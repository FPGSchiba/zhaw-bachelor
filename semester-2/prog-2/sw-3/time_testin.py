import datetime

print(datetime.datetime.now().second)
x, _ = divmod(datetime.datetime.now().second, 10)

print(x)

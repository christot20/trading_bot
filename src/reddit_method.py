import requests

from helpers import checkTime

# maybe try to make this a class?
def reddit_mode(func):
    # do something to check if it is 9:30 to 4 and if it is a weekday so it can trade
    # also do something so that it's checking the url every 5 mins

    # Maybe make powershell script to start (python .\src\bot.py) and stop (ctrl + c) the bot
    # at certain times? (9:30 to 4 on weekdays)
    # then use while true for this whole function and have stuff for making it work above (i.e. classes and helpers)
    while True:
        time = func()
        if time == '23:57:00':  # check if matches with the desired time
            print('sending message')
            url = "https://apewisdom.io/api/v1.0/filter/wallstreetbets/page/1"
            r =  requests.get(url)
            data = r.json()
            stocks = list(data.values())[3]
            print(stocks[:5])
        if time == '23:58:00': ## WORKS!!
            break
#print(sorted(data, key=data.get, reverse=True)[:5])



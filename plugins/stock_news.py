import requests
from datetime import datetime as dt, timedelta
# import os
# from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = "https://www.alphavantage.co/query"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    # "apikey": "9G97O5JU5ZUCI5E7",
    "apikey": "demo"
}

stock_return = requests.get(STOCK_API, params=stock_params).json()
print(stock_return)
tod = dt.today()
today = tod.strftime("%d-%m-%Y")


def get_stock_prices(stock_return, start_date, days_to_check=5):
    for i in range(1, days_to_check + 1):
        yesterday = (start_date - timedelta(days=i)).strftime("%Y-%m-%d")
        previous_day = (start_date - timedelta(days=i + 1)).strftime("%Y-%m-%d")
        try:
            yesterday_close_price = stock_return["Time Series (Daily)"][yesterday]["4. close"]
            previous_close_price = stock_return["Time Series (Daily)"][previous_day]["4. close"]
            return yesterday_close_price, previous_close_price, previous_day
        except KeyError:
            continue  # Try the next pair of dates
    raise KeyError(f"Valid dates not found in the last {days_to_check} days")


def check_difference(yest_close, prev_close) -> str:
    difference = prev_close - yest_close
    percentage = (difference / prev_close) * 100
    if prev_close > yest_close:
        change = f" 🔻{round(percentage, 2)}%"
        print(f"There was an decrease in the stock by {round(percentage, 2)}%.")
    else:
        change = f" 🔺{round(percentage, 2) * -1}%"
        print(f"There was a increase in the stock by {round(percentage, 2)}%.")
    return change


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

NEWS_API = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "bf592dc0f15a4b97960927a3d666a41e"



def finish_all() -> str:
    try:
        yesterday_close_price, previous_close_price, prev_day = get_stock_prices(stock_return, tod)
        print(yesterday_close_price, previous_close_price)
    except KeyError as e:
        print(e)

    differ = check_difference(float(yesterday_close_price), float(previous_close_price))

    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "from": f"{prev_day}",
        "sortBy": "relevancy",
        "searchIn": "title"
    }

    news_return = requests.get(url=NEWS_API, params=news_params).json()
    article_list = news_return["articles"][0]
    headline = article_list["title"]
    content = article_list['description']
    msg = f"""
TSLA: {differ}

Headline: {headline}

Brief: {content}
"""


    


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

# ***REMOVED***
# ***REMOVED***
# client = Client(account_sid, auth_token)

# message = client.messages \
#     .create(
#          body=f'{msg}',
#          from_='+13312598533',
#          to='+256742676696'
#      )

# print(message.sid)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


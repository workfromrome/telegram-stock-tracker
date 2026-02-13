from datetime import date, timedelta
import requests
import math
import os


TG_TOKEN = os.environ.get('TELEGRAM_TOKEN')
MY_ID = os.environ.get('TELEGRAM_CHAT_ID')
STOCK_API_KEY = os.environ.get('STOCK_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')


STOCK = "NVDA"
COMPANY_NAME = "Nvidia"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


yesterday = str(date.today() - timedelta(days=1))
before_yest = str(date.today() - timedelta(days=2))
last_week = str(date.today() - timedelta(days=7))

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

news_params = {
    "qInTitle": COMPANY_NAME,
    "from": last_week,
    "sortBy": "popularity",
    "language": "en",
    "pageSize": "3",
    "apiKey": NEWS_API_KEY,
}

av_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
av_response.raise_for_status()
stock_data = av_response.json()
stock_yest = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])
stock_bf_yest = float(stock_data["Time Series (Daily)"][before_yest]["4. close"])
percentage_change = math.floor(((stock_yest - stock_bf_yest) / stock_bf_yest) * 100)


if abs(percentage_change) >= 5:

    if percentage_change > 0:
        stock_value_emoji = "🔺"
    else:
        stock_value_emoji = "🔻"

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    news_dict = news_data["articles"]
    msg = f"{STOCK}:  {math.floor(percentage_change)}% {stock_value_emoji}\n"

    for article in news_dict:
        msg += (f"HeadLine: {article['title']}\n"
                f"Brief: {article['description']}\n\n")

    telegram_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    telegram_text = {
        "chat_id": MY_ID,
        "text": f"{msg}"
    }
    requests.post(url=telegram_url, data=telegram_text)

telegram_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
telegram_text = {
    "chat_id": MY_ID,
    "text": "Test!"
}
requests.post(url=telegram_url, data=telegram_text)


import requests
from dotenv import dotenv_values
from sms import Sms

config = dotenv_values()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
MY_NUMBER = config.get('MY_NUMBER')
STOCK_API_KEY = config.get('STOCK_API_KEY')
NEW_API_KEY = config.get('NEW_API_KEY')

STOCK_API_URL = "https://www.alphavantage.co/query"
NEWS_API_URL = "https://newsapi.org/v2/everything"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
    "datatype": "json"
}
news_parameters = {
    "apiKey": NEW_API_KEY,
    "qInTitle": STOCK
}


def send_request(url, params):
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    data = response.json()
    return data


def change_stock_price():
    data = send_request(STOCK_API_URL, stock_parameters)
    stock_data = data['Time Series (Daily)']
    stock_data_list = [value for (key, value) in stock_data.items()]
    yesterday_closing_price = stock_data_list[0]['4. close']
    previous_day_closing_price = stock_data_list[1]['4. close']
    positive_change = abs(float(yesterday_closing_price) - float(previous_day_closing_price))
    percent_change = positive_change / float(yesterday_closing_price) * 100
    return percent_change


def get_news():
    news_data = send_request(NEWS_API_URL, news_parameters)
    news_list = news_data['articles'][:3]
    data = [f"Headline:{article['title']}.\n Brief:{article['description']} " for article in news_list]
    return data


stock_change = change_stock_price()
if stock_change > 5:
    news = get_news()
    for new in news:
        message = f"{COMPANY_NAME}: {stock_change}\n"
        message += new
        sms = Sms(MY_NUMBER, message)
        print("sent")
        # send text


import json
from random import choice
import schedule
import time
import logging


def getAuth() -> dict:
    with open("./static/profile.json") as f:
        profile = json.load(f)
    return profile


def getRandomTicker() -> str:
    with open("./static/tickers.json") as f:
        data = json.load(f)
        stock = choice(data)
    return stock


def checkMarketOpen() -> bool:
    isOpen = False
    return isOpen


def buyStock(ticker: str) -> bool:
    print("We bought", ticker)
    return True


def sellStock(ticker: str) -> bool:
    print("We sold", ticker)
    return True


def excecuteTrade() -> bool:
    if checkMarketOpen():
        sellStock()
        logging.info('Sold: {} for {}'.format("", 0))
        ticker = getRandomTicker()
        buyStock(ticker)
        logging.info('Bought: {} for {}'.format(ticker, 0))
    logging.warning('Trade called during market close')


def runBot():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    schedule.every(1).seconds.do(excecuteTrade)
    logging.basicConfig(filename='./logs/trades.log',
                        encoding='utf-8', format='%(asctime)s %(message)s', level=logging.INFO)
    runBot()

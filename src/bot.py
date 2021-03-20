import schedule
import time
import logging
from local.interactions import *
import robin_stocks.robinhood as robinhood
from pyotp import TOTP


def checkMarketOpen() -> bool:
    isOpen = True
    return isOpen


def buyStock(ticker: str) -> bool:
    print("We bought", ticker)
    logging.info('Bought: {} for {}'.format(ticker, 0))
    return True


def sellStock(stock: dict) -> bool:
    logging.info('Sold: {} for {} making {}'.format(
        stock["ticker"], 0, 0 - stock["purchase_price"]))
    return True


def excecuteTrade() -> bool:
    if checkMarketOpen():
        stock = getPositions()[0]
        sellStock(stock)
        ticker = getRandomTicker()
        buyStock(ticker)
    else:
        logging.warning('Trade called during market close')


def runBot():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    user, password, limit, totp_string = getAuth().values()
    totp = TOTP(totp_string).now()
    print(user, password)
    login = robinhood.login(user, password, mfa_code=totp)
    print(login)
    schedule.every(1).seconds.do(excecuteTrade)
    logging.basicConfig(filename='./logs/trades.log',
                        encoding='utf-8', format='%(asctime)s %(message)s', level=logging.INFO)
    # runBot()

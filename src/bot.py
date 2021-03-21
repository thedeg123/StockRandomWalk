import schedule
import time
import logging
from local.interactions import *
import robin_stocks.robinhood as robinhood
from pyotp import TOTP


def login():
    user, password, limit, totp_string = getAuth().values()
    totp = TOTP(totp_string).now()
    login = robinhood.login(user, password, mfa_code=totp)


def checkMarketOpen() -> bool:
    hours = robinhood.get_market_today_hours("XNYS")
    return hours["is_open"]


def buyStock(ticker: str) -> bool:
    order = robinhood.order_buy_crypto_by_price(ticker, 1)
    if 'id' not in order.keys():
        logging.info('Failed to buy: {}'.format(order))
        return False
    else:
        print("bought", order)
        logging.info('Bought: {} shares of {} for {}'.format(
            order["quantity"], ticker, order["price"]))
        setPositions(ticker, order["price"], order["quantity"])
    return True


def sellStock(stock: dict) -> bool:
    order = robinhood.order_sell_crypto_by_price(stock["ticker"], 1)
    if 'id' not in order.keys():
        logging.info('Failed to buy: {}'.format(order))
        return False
    else:
        print("sold", order)
        beta = float(stock["quantity"]) * \
            (float(order["price"]) - float(stock["purchase_price"]))
        logging.info('Sold: {} for {} making {}'.format(
            stock["ticker"], float(order["price"]), beta))
    return True


def excecuteTrade() -> bool:
    login()
    if True:
        stock = getPositions()[0]
        sellStock(stock)
        time.sleep(120)
        ticker = getRandomTicker()
        buyStock(ticker)
    else:
        logging.warning('Trade called during market close')


def runBot():
    time.sleep(1)
    schedule.run_pending()


if __name__ == "__main__":
    schedule.every(1).seconds.do(excecuteTrade)
    logging.basicConfig(filename='./logs/trades.log',
                        encoding='utf-8', format='%(asctime)s %(message)s', level=logging.INFO)
    runBot()

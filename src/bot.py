import time
import logging
from local.interactions import *
import robin_stocks.robinhood as robinhood
from pyotp import TOTP
from datetime import datetime


def login():
    user, password, limit, totp_string, rate = getProfile().values()
    totp = TOTP(totp_string).now()
    login = robinhood.login(user, password, mfa_code=totp)


def checkMarketOpen() -> bool:
    hours = robinhood.get_market_today_hours("XNYS")
    mktOpen = datetime.strptime(hours["opens_at"], "%Y-%m-%dT%H:%M:%SZ")
    mktClose = datetime.strptime(hours["opens_at"], "%Y-%m-%dT%H:%M:%SZ")
    return hours["is_open"] and mktOpen < datetime.now() < mktClose


def buyStock(ticker: str) -> bool:
    order = robinhood.order_buy_fractional_by_price(
        ticker, getProfile()["trade_limit"])
    if 'id' not in order.keys():
        logging.info('Failed to buy: {}'.format(order))
        return False
    else:
        logging.info('Bought: {} shares of {} for {}'.format(
            order["quantity"], ticker, order["price"]))
        setPositions(ticker, order["price"], order["quantity"])
    return True


def sellStock(stock: dict) -> bool:
    order = robinhood.order_sell_fractional_by_price(
        stock["ticker"], stock["quantity"])
    if 'id' not in order.keys():
        logging.info('Failed to buy: {}'.format(order))
        return False
    else:
        beta = float(stock["quantity"]) * \
            (float(order["price"]) - float(stock["purchase_price"]))
        logging.info('Sold: {} for {} making {}'.format(
            stock["ticker"], float(order["price"]), beta))
    return True


def allowOrder() -> bool:
    '''
    We dont want to buy/sell before our last order is complete
    If an order is not complete we do nothing
    '''
    if not checkMarketOpen():
        logging.warning('Trade called during market close')
        return False
    orders = robinhood.get_all_open_stock_orders()
    if orders:
        logging.warning(
            'Trade called before previus order for {} closed, since: {}'.format(
                getPositions()[0]["ticker"], orders[0]["created_at"]))
        return False
    return True


def excecuteTrade(orderType: str) -> bool:
    login()
    if allowOrder():
        if orderType == "sell":
            stock = getPositions()[0]
            res = sellStock(stock)
        else:
            ticker = getRandomTicker()
            res = buyStock(ticker)
        if res:
            setHolding(orderType == "buy")
        return res


def runBot(rate: int):
    while True:
        excecuteTrade("sell" if getHolding() else "buy")
        time.sleep(rate)


if __name__ == "__main__":
    logging.basicConfig(filename='./logs/trades.log',
                        encoding='utf-8', format='%(asctime)s %(message)s', level=logging.INFO)
    runBot(getProfile()["trade_rate"])


'''
want to set next trade with amount secured from last trade only after last trade was excecuted 
'''

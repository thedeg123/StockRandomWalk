import time
import logging
from local.interactions import *
import robin_stocks.robinhood as robinhood
from pyotp import TOTP
from datetime import datetime

CRYPTO = False


def login():
    user, password, limit, totp_string, rate = getProfile().values()
    totp = TOTP(totp_string).now()
    login = robinhood.login(user, password, mfa_code=totp)


def getNextMarketOpen() -> bool:
    if CRYPTO:
        return datetime.utcnow()
    hours = robinhood.get_market_next_open_hours("XNYS")
    mktOpen = datetime.strptime(hours["opens_at"], "%Y-%m-%dT%H:%M:%SZ")
    return mktOpen


def checkMarketOpen() -> bool:
    if CRYPTO:
        return True
    hours = robinhood.get_market_today_hours("XNYS")
    mktOpen = datetime.strptime(hours["opens_at"], "%Y-%m-%dT%H:%M:%SZ")
    mktClose = datetime.strptime(hours["closes_at"], "%Y-%m-%dT%H:%M:%SZ")
    return hours["is_open"] and mktOpen < datetime.utcnow() < mktClose


def buyStock(ticker: str) -> bool:
    purchaseAmount = getPurchasePower() or getProfile()["trade_limit"]
    if CRYPTO:
        order = robinhood.order_buy_crypto_by_price(
            ticker, purchaseAmount)
    else:
        order = robinhood.order_buy_fractional_by_price(
            ticker, purchaseAmount)

    if 'id' not in order.keys():
        logging.info('Failed to buy: {}'.format(order))
        return False
    else:
        logging.info('Bought: {} shares of {} for {}'.format(
            order["quantity"], ticker, order["price"]))
        setPositions(ticker, order["price"], order["quantity"])
        setHolding(True)
    return True


def sellStock(stock: dict) -> bool:
    if CRYPTO:
        order = robinhood.order_sell_crypto_by_quantity(
            stock["ticker"], float(stock["quantity"]))
    else:
        order = robinhood.order_sell_fractional_by_quantity(
            stock["ticker"], float(stock["quantity"]))
    if 'id' not in order.keys():
        logging.info('Failed to sell: {}'.format(order))
        return False
    else:
        revenue = float(stock["quantity"]) * float(order["price"])
        beta = float(stock["quantity"]) * \
            (float(order["price"]) - float(stock["purchase_price"]))
        logging.info('Sold: {} for {} making {}'.format(
            stock["ticker"], float(order["price"]), beta))
        setHolding(False)
        setPurchasePower(revenue)
    return True


def allowOrder() -> bool:
    '''
    We dont want to buy/sell before our last order is complete
    If an order is not complete we do nothing
    '''
    if not checkMarketOpen():
        logging.warning('Trade called during market close')
        return False, "market_close"
    if CRYPTO:
        orders = robinhood.get_all_open_crypto_orders()
    else:
        orders = robinhood.get_all_open_stock_orders()
    if orders:
        logging.warning(
            'Trade called before previus order for {} closed, since: {}'.format(
                getPositions()[0]["ticker"], orders[0]["created_at"]))
        return False, "ticket_open"
    return True, ""


def excecuteTrade(orderType: str) -> bool:
    login()
    allowed, reason = allowOrder()
    if allowed:
        if orderType == "sell":
            stock = getPositions()[0]
            return sellStock(stock), ""
        else:
            ticker = getRandomTicker(crypto=CRYPTO)
            return buyStock(ticker), ""
    return False, reason


def runBot(rate: int):
    '''
    In a tik tok fashion we buy, hold for time rate, sell, wait for 2 minutes, buy etc
    '''
    while True:
        result, reason = excecuteTrade("sell" if getHolding() else "buy")
        off_hold_wait = 120
        if reason == "market_close":
            off_hold_wait = (getNextMarketOpen() - datetime.utcnow()).seconds
        time.sleep(rate if getHolding() else off_hold_wait)


if __name__ == "__main__":
    logging.basicConfig(filename='./logs/trades.log',
                        encoding='utf-8', format='%(asctime)s %(message)s', level=logging.INFO)
    rate = float(getProfile()["trade_rate"])
    if rate < 60:
        raise ValueError(
            "Trade rate must be at least 1 minute but was {}".format(rate))
    runBot(rate)

#!/usr/bin/env python2
#
#by Eduardo"

'''
This script calls the tick endpoint of 10 different markets, and saves their
current (ask + bid) /2 value to a database. The table has shape:

CREATE TABLE IF NOT EXISTS tick_data_minute
    (timestamp DATE PRIMARY KEY,
    bitfinex DOUBLE,
    binance DOUBLE,
    okex DOUBLE,
    huobi DOUBLE,
    bitz DOUBLE,
    coinbene DOUBLE,
    zb DOUBLE,
    bitmart DOUBLE,
    idax DOUBLE,
    bibox DOUBLE);

'''

from __future__ import absolute_import
import urllib
import requests
import json
import base64
import hmac
import hashlib
import time
import datetime
import sqlite3

TIMEOUT = 8.0

def ping_bitfinex(symbol='btcusd'):
    pass
    '''
    Get mid data point for bitfinex
    https://docs.bitfinex.com/v1/reference#rest-public-ticker
    '''
    url = ('https://api.bitfinex.com/v1/pubticker/'+symbol)

    try:
        j = requests.get(url, timeout=TIMEOUT).json()
        j = (float(j['ask']) + float(j['bid']))/2
    except:
        j = 0

    return j

def ping_binance(symbol='BTCUSDT'):
    pass
    '''
    Get binance mid datapoint
    https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
    '''
    url = ('https://api.binance.com/api/v1/ticker/24hr?symbol='+symbol)
    try:
        j = requests.get(url, timeout=TIMEOUT).json()
        j = (float(j['askPrice'])+float(j['bidPrice']))/2
    except:
        j = 0
    return j

def ping_okex(symbol='btc_usd'):
    pass
    '''
    Get mid data point for okex
    https://support.okcoin.com/hc/en-us/articles/360000697832-REST-API-Reference
    '''
    url = ('https://www.okcoin.com/api/v1/ticker.do?symbol=' + symbol)

    try:
        j = requests.get(url, timeout=TIMEOUT).json()['ticker']
        j = (float(j['buy']) + float(j['sell']))/2
    except:
        j = 0

    return j

def ping_huobi(symbol='BTC_CQ'):
    pass
    '''
    Get mid data point from huobi
    https://github.com/huobiapi/API_Docs_en/wiki/REST_Reference#get-markettickers
    '''

    url = ('https://api.hbdm.com/market/detail/merged?symbol='+symbol)

    try:
        j = requests.get(url, timeout=TIMEOUT).json()['tick']
        j = (float(j['ask'][0]) + float(j['bid'][0]))/2
    except:
        j = 0
    return j

def ping_bitz(symbol='btc_usdt'):
    pass
    '''
    Get mid data point for bitz
    https://apidoc.bit-z.com/en/market-quotation-data/Get-ticker-data.html
    '''
    url = ('https://apiv2.bitz.com/Market/ticker?symbol='+symbol)
    try:
        j = requests.get(url, timeout=TIMEOUT).json()['data']
        j = (float(j['askPrice']) + float(j['bidPrice']))/2
    except:
        j = 0
    return j

def ping_coinbene(symbol='btcusdt'):
    pass
    '''
    Get mid data point from coinbene
    https://github.com/Coinbene
    '''
    url = ('http://api.coinbene.com/v1/market/ticker?symbol='+symbol)

    try:
        j = requests.get(url, timeout=TIMEOUT).json()['ticker'][0]
        j = (float(j['ask']) + float(j['bid']))/2
    except:
        j = 0
    return j

def ping_zb(symbol='btc_usdt'):
    pass
    '''
    Get bid+asl/2 from zb
    https://www.zb.com/i/developer/restApi
    '''
    url = ('http://api.zb.cn/data/v1/ticker?market='+symbol)
    try:
        j = requests.get(url, timeout=TIMEOUT).json()['ticker']
        j = (float(j['sell']) + float(j['buy']))/2
    except:
        j = 0
    return j

def ping_lbank(symbol='all'):
    pass
    '''
    Get ask+bid/2 from lbank [NOT WORKING]
    https://github.com/LBank-exchange/lbank-official-api-docs
    '''
    parameters = {'symbol': symbol}
    url = ('https://api.lbkex.com/v1/ticker.do&'+str(urllib.urlencode(parameters)))
    #print(url)
    try:
        j = requests.get(url, timeout=TIMEOUT)#.json()
        #print(j)
    except:
        j = 0
    return j

def ping_bitmart(symbol='BTC_USDT'):
    pass
    '''
    get ask+bid/2 data from bitmart
    https://github.com/bitmartexchange/api-docs/blob/master/rest/public/ticker.md
    '''
    url = ('https://openapi.bitmart.com/v2/ticker?symbol='+symbol)
    try:
        j = requests.get(url, timeout=TIMEOUT).json()
        j = (float(j['bid_1']) + float(j['ask_1']))/2
    except:
        j = 0
    return j

def ping_idax(symbol='BTC_USDT'):
    pass
    '''
    Get ask+bid/2 data point from idax
    https://github.com/idax-exchange/idax-official-api-docs/blob/master/open-api_en.md#11-ticker-price
    '''
    url = ('https://openapi.idax.pro/api/v2/ticker?pair='+symbol)
    try:
        j = requests.get(url, timeout=TIMEOUT).json()['ticker'][0]
        j = (float(j['high']) + float(j['low']))/2
    except:
        j = 0
    return j

def ping_bibox(symbol='BTC_USDT'):
    pass
    '''
    Get bibox mid price
    https://github.com/Biboxcom/API_Docs_en/wiki
    '''
    url = (' https://api.bibox.com/v1/mdata?cmd=ticker&pair='+symbol)
    try:
        j = requests.get(url, timeout=TIMEOUT).json()['result']
        j = (float(j['sell'])+float(j['buy']))/2
    except:
        j = 0
    return j

if __name__ == '__main__':
    pass
    '''
    Get values
    '''
    timestamp = datetime.datetime.now()
    bitfinex = ping_bitfinex()
    binance = ping_binance()
    okex = ping_okex()
    huobi = ping_huobi()
    bitz = ping_bitz()
    coinbene = ping_coinbene()
    zb = ping_zb()
    bitmart = ping_bitmart()
    idax = ping_idax()
    bibox = ping_bibox()

    '''
    Create sqlite command to add all the values
    '''
    db = sqlite3.connect('tick_data_minute.db')
    c = db.cursor()
    command = 'CREATE TABLE IF NOT EXISTS tick_data_minute '
    command += '(timestamp DATE PRIMARY KEY, '
    command += 'bitfinex DOUBLE, '
    command += 'binance DOUBLE, '
    command += 'okex DOUBLE, '
    command += 'huobi DOUBLE, '
    command += 'bitz DOUBLE, '
    command += 'coinbene DOUBLE, '
    command += 'zb DOUBLE, '
    command += 'bitmart DOUBLE, '
    command += 'idax DOUBLE, '
    command += 'bibox DOUBLE);'
    c.execute(command)

    command = 'INSERT INTO tick_data_minute '
    command += '(timestamp, bitfinex, binance, okex, huobi, bitz, coinbene, zb, bitmart, idax, bibox)'
    command += ' VALUES '
    command += '(\'' + str(timestamp) + '\', '
    command += str(bitfinex) + ', '
    command += str(binance) + ', '
    command += str(okex) + ', '
    command += str(huobi) + ', '
    command += str(bitz) + ', '
    command += str(coinbene) + ', '
    command += str(zb) + ', '
    command += str(bitmart) + ', '
    command += str(idax) + ', '
    command += str(bibox) + ');'
    c.execute(command)
    db.commit()
    db.close()
    '''
    For debugging purposes
    '''
    #print(command)
    #print(timestamp)
    #print('bitfinex: ', bitfinex)
    #print('binance: ', binance)
    #print('okex: ', okex)
    #print('huobi: ', huobi)
    #print('bitz: ', bitz)
    #print('coinbene: ', coinbene)
    #print('zb: ', zb)
    #print('bitmart: ', bitmart)
    #print('idax: ', idax)
    #print('bibox: ', bibox)

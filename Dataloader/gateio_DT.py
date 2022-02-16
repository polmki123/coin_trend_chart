# !/usr/bin/env python
# coding: utf-8
import logging
import random
import os
import csv
import numpy as np
import pandas as pd
import datetime 
import sys
import time
import threading
import concurrent.futures
import sqlite3

from decimal import Decimal as D, ROUND_UP, getcontext

from gate_api import ApiClient, Configuration, Loan, MarginApi, Order, RepayRequest, SpotApi, Transfer, WalletApi
from gate_api.exceptions import GateApiException

# sys.path.append(os.path.abspath(os.path.dirname(__file__))) #상위 경로 추가 
def load_sql_data(coin, interval, limit = '52' ) :
    current_path = os.path.dirname(__file__)
    path = os.path.join( current_path, 'gate_Dt' ) 
    con = sqlite3.connect( os.path.join( path , interval, "data.db") )
    Data = pd.read_sql_query("SELECT * FROM %s ORDER BY date desc LIMIT %s;" % ( ('\'' + coin.replace("KRW-", "") + '\'')  , limit ) , con )
    return Data

class Accumerate_data :
    
    config = Configuration(key="", secret="")
    spot_api = SpotApi(ApiClient(config))
    def __init__(self, ticker, interval= '1d'):
        self.ticker = ticker
        self.interval = str(interval)
        current_path = os.path.dirname(__file__)
        self.home = os.path.join( current_path, 'gate_Dt' ) 
        if not os.path.exists( os.path.join( self.home, interval) ): os.makedirs( os.path.join( self.home, interval) )

    def _set_data(self, ticker, interval):
        con = sqlite3.connect( os.path.join( self.home , interval, "data.db") )
        cur = con.cursor()
        try :
            query = cur.execute("SELECT * FROM %s ORDER BY date desc LIMIT 1;" % ( ('\'' + ticker + '\'')  ))
            before = query.fetchall()[0][0]
        except :
            before = None
        yesterday = datetime.datetime.today() - datetime.timedelta(120)
        yesterday = int ( time.mktime ( yesterday.timetuple() ) )
        print(yesterday)
        current  = self.spot_api.kline_list_candletrade(currency_pair = ticker, interval = interval, _from = yesterday)
        print( "current len " , len(current))
        return before, current

    @classmethod
    def rebuild_data(cls, data):
        # 'time'  '총 거래 대금' '종가' '고가' 저가' '시작가'
        #['1636070400', '162518.88280499349', '3.695', '4.35', '3', '4.184']
        data = pd.DataFrame( data = 
                                        {
                                            'date'                  : [ float(i[0 ]) for i in data] ,
                                            'volume'                : [ float(i[1 ]) for i in data] ,
                                            'close'                 : [ float(i[2 ]) for i in data] ,
                                            'high'                  : [ float(i[3 ]) for i in data] , 
                                            'low'                   : [ float(i[4 ]) for i in data] ,
                                            'open'                  : [ float(i[5 ]) for i in data] ,
                                        }
                                   )
        data = data.set_index('date')
        return data

    @staticmethod
    def printALL(data):
        print( 'data', len(data)   )
        print( data[-1])

    def cmp_time_Data(self, before, current, interval, ticker):
        # try :
        last_time = datetime.datetime.fromtimestamp( before )
        Add_Time  = datetime.datetime.fromtimestamp( current.index[-1] )
        now       = datetime.datetime.now()
        print(before, current.index[-1])
        print('last_time',last_time, 'Add_Time', Add_Time)
        print(interval)

        # 데이터는 시간이 완료 된 직후에 쌓이기 때문에 바로 저장하지 말고 그 다음 시간에 저장해야한다. 
        if 'm' in self.interval :
            minutes_rest = now.minute % int(self.interval.replace('m',''))
            now = now - datetime.timedelta(minutes=minutes_rest) 
            if Add_Time > last_time and Add_Time.hour == now.hour and Add_Time.minute == now.minute and Add_Time.day == now.day :
                print("save new Data")
                self.writeFile(interval, before, current.iloc[: -1], ticker)
                return True
        elif 'h' in self.interval :
            hour_rest = now.hour % int(self.interval.replace('h',''))
            now = now - datetime.timedelta(hours=hour_rest) 
            if Add_Time > last_time and Add_Time.hour == now.hour and Add_Time.day == now.day :
                print("save new Data")
                self.writeFile(interval, before, current.iloc[: -1], ticker)
                return True
        elif 'd' in self.interval :
            day_rest = now.day % int(self.interval.replace('d',''))
            now = now - datetime.timedelta(days=day_rest) 
            if Add_Time > last_time and Add_Time.day == now.day :
                print("save new Data")
                self.writeFile(interval, before, current.iloc[: -1], ticker)
                return True

        if Add_Time > last_time :
            print("시간은 같지만 현재 최근값 ")
            self.writeFile(interval, before, current , ticker)
            return True

        return False

    def writeFile(self, interval, before, current, ticker):
        print(ticker)
        con = sqlite3.connect( os.path.join( self.home , interval, "data.db") )
        last_time = datetime.datetime.fromtimestamp( before ) 
        for i in range(0, len(current)) :
            new = datetime.datetime.fromtimestamp( current.index[i] )  
            if new > last_time :
                # print(current.iloc[i:])
                current.iloc[i:].astype('float32').to_sql(ticker, con, if_exists='append')
                break

    def NewFile(self, interval, current, ticker):
        print("new data save")
        con = sqlite3.connect( os.path.join( self.home , interval, "data.db") )
        current.iloc[: -1].astype('float32').to_sql(ticker, con, if_exists='append')
        return True

    def write_real_data(self, ticker, interval):
        before, current = self._set_data(ticker, self.interval)
        current = self.rebuild_data(current)
        if before == None :
            return self.NewFile(interval, current, ticker)
        return self.cmp_time_Data(before, current, self.interval, ticker )

    def make_ticker(self, Market_Coin) :
        trade_coin = []
        for _ticker in Market_Coin : 
            print(_ticker)
            while 1 :
                try :
                    self.write_real_data(_ticker, self.interval )
                    trade_coin.append(_ticker)
                    break
                except :
                    print("wait a moment")
                    time.sleep(10)
                    self.write_real_data(_ticker, self.interval )
                    trade_coin.append(_ticker)
                    break

        return trade_coin

    def start(self):
        check_p = 0
        trade_coin = []
        trade_coin = self.make_ticker(self.ticker)
        return trade_coin

if __name__ == '__main__':
    config = Configuration(key="", secret="")
    spot_api = SpotApi(ApiClient(config))
    pair = spot_api.list_tickers()
    ticker = []
    for _pair in pair :
        if 'USDT' in _pair.currency_pair and '3S' not in _pair.currency_pair and '3L' not in _pair.currency_pair :
            ticker.append( _pair.currency_pair )
    
    ticker.remove('BCHA_USDT')
    for _i in [ '4h', '8h' ] :
        gateio_dt = Accumerate_data(ticker, _i) 
        print(gateio_dt.start())
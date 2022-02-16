# orderbook_0.py
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import time
import os 

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('__file__')))) #상위 경로 추가 
from util.binance_coin import *
from Dataloader.gateio_DT import *
from util.gateio_coins import * 

def ts_to_date(_date):
    _date = datetime.datetime.fromtimestamp(_date)
    format = '%m-%d'
    str_datetime = datetime.datetime.strftime(_date,format)
    return str_datetime

def check_volume_data ( interval, limit = '60' ) :
    # {
    #     'date'                  : [ float(i[0 ]) for i in data] ,
    #     'volume'                : [ float(i[1 ]) for i in data] ,
    #     'close'                 : [ float(i[2 ]) for i in data] ,
    #     'high'                  : [ float(i[3 ]) for i in data] , 
    #     'low'                   : [ float(i[4 ]) for i in data] ,
    #     'open'                  : [ float(i[5 ]) for i in data] ,
    # }
    ticker = list(coin_cap_id.keys())
    list_coin = []
    pump_stock = []
    period = 7

    for _coin in ticker :
        try :
            data = load_sql_data(_coin, interval, limit = limit )
            data = data[::-1]
            # biggest_volume(list_coin, pump_stock, period, _coin, data) 
            Volume_increase(list_coin, pump_stock, period, _coin, data)
            # BTC_CMP_CH(list_coin, pump_stock, interval, period, _coin, data)
        except :
            continue
    print( interval, " list_coin :" , list_coin, len(list_coin))
    return pump_stock


def BTC_CMP_CH(list_coin, pump_stock, interval, period, _coin, data):
    BT_DA = load_sql_data( 'BTC_USDT', interval, limit = period )
    bt_p_ch = (BT_DA.iloc[-1].close - BT_DA.iloc[0].open) / BT_DA.iloc[0].open  * 100
    cn_p_ch = (data.iloc[-1].close - data.iloc[-period].open) / data.iloc[0].open  * 100
    
    print( bt_p_ch, cn_p_ch )
    if cn_p_ch > bt_p_ch :
        data['change'] = data.close.pct_change()*100
        data.date = data.date.apply(ts_to_date)
        data = data.fillna(0)
                # print(_coin)
                # print(data)
        list_coin.append(_coin)
        pump_stock.append( { 'coin' : _coin, 'data' : data } , )            

def Volume_increase(list_coin, pump_stock, period, _coin, data):
    print(_coin)
    for i in range( 0, period ) :
        std = data.iloc[ -1 - i ] 
        # bck = data.iloc[-2 - i] 
        bck = data.iloc[ -1 - i - ( period - i ): ].sort_values(ascending = False, by = 'volume').iloc[-1]
        # print( std.close, bck.close, std.volume, bck.volume, ts_to_date(bck.date)   )
        if std.close > bck.close * 1.01 and std.volume > bck.volume * 3 and ( std.high + std.low) / 2 * std.volume > 3000000 :
            # and data.iloc[-1].close * 1.05 < std.high :
            # print( 'std', std, datetime.datetime.fromtimestamp(std.date) )
            # print( 'bck', bck, datetime.datetime.fromtimestamp(bck.date) )
                    # data = load_sql_data(_coin, interval, limit = '7' )
                    # data = data[::-1]
            data['change'] = data.close.pct_change()*100
            data.date = data.date.apply(ts_to_date)
            data = data.fillna(0)
            list_coin.append(_coin)
            pump_stock.append( { 'coin' : _coin, 'data' : data } , )
            break 
        else :
            if std.close > bck.close * 1.01 and std.volume > bck.volume * 5 and  ( std.high + std.low) / 2 * std.volume > 300000 :
                # data.iloc[-1].close * 1.05 < std.high and:
                data['change'] = data.close.pct_change()*100
                data.date = data.date.apply(ts_to_date)
                data = data.fillna(0)
                        # print(_coin)
                        # print(data)
                list_coin.append(_coin)
                pump_stock.append( { 'coin' : _coin, 'data' : data } , )
                break
                
def biggest_volume(list_coin, pump_stock, period, _coin, data):
    b_volume = data.sort_values(ascending = False, by = 'volume').iloc[:2]
    v_change = False
    for _b in b_volume.date :
        for _d in data.iloc[-period : ].date :
            if _b == _d :
                v_change = True
                break

    if v_change == True :
        recent_data = data.iloc[ -period : ].sort_values(ascending = False, by = 'volume').iloc[:2]
        for i in range(len(recent_data)) :
            _rc = recent_data.iloc[i].close
            if data.iloc[-1].close < _rc * 1.1 and recent_data.iloc[i].volume * ( recent_data.iloc[i].high + recent_data.iloc[i].low) / 2  > 1000000 :
                        # data = load_sql_data(_coin, interval, limit = '7' )
                        # data = data[::-1]
                data['change'] = data.close.pct_change()*100
                data.date = data.date.apply(ts_to_date)
                data = data.fillna(0)
                        # print(_coin)
                        # print(data)
                list_coin.append(_coin)
                pump_stock.append( { 'coin' : _coin, 'data' : data } , )
                break 
            else :
                if (data.iloc[i-1].volume * 5 <  data.iloc[i].volume) and (data.iloc[i-1].close * 1.05 < data.iloc[i].close):
                    data['change'] = data.close.pct_change()*100
                    data.date = data.date.apply(ts_to_date)
                    data = data.fillna(0)
                            # print(_coin)
                            # print(data)
                    list_coin.append(_coin)
                    pump_stock.append( { 'coin' : _coin, 'data' : data } , )
                    break


def check_candle_data ( interval, limit = '90' ) :
    # {
    #     'date'                  : [ float(i[0 ]) for i in data] ,
    #     'volume'                : [ float(i[1 ]) for i in data] ,
    #     'close'                 : [ float(i[2 ]) for i in data] ,
    #     'high'                  : [ float(i[3 ]) for i in data] , 
    #     'low'                   : [ float(i[4 ]) for i in data] ,
    #     'open'                  : [ float(i[5 ]) for i in data] ,
    # }
    ticker = list(coin_cap_id.keys())
    list_coin = []
    pump_stock = []
    period = 10
    for _coin in ticker :
        try :
            data = load_sql_data(_coin, interval, limit = limit )
            data = data[::-1]
            b_volume = data.sort_values(ascending = False, by = 'volume').iloc[:2]
            v_change = False
            for _b in b_volume.date :
                for _d in data.iloc[ -period: -4 ].date :
                    if _b == _d :
                        v_change = True
                        break

            if v_change == True :
                recent_data = data.iloc[ -period: -4 ].sort_values(ascending = False, by = 'volume').iloc[:2]
                for i in range(len(recent_data)) :
                    _rc = recent_data.iloc[i].close
                    if data.iloc[-1].close < _rc * 1.1 and recent_data.iloc[i].volume * ( recent_data.iloc[i].high + recent_data.iloc[i].low) / 2 > 1000000:
                        data['change'] = data.close.pct_change()*100
                        data.date = data.date.apply(ts_to_date)
                        data = data.fillna(0)
                        # print(_coin)
                        # print(data)
                        list_coin.append(_coin)
                        pump_stock.append( { 'coin' : _coin, 'data' : data } , )
                        break 
        except :
            continue
    print( interval, " list_coin :" , list_coin)
    return pump_stock

def time_checker(interval, before, now) :
    date_now = datetime.datetime.fromtimestamp(now) 
    date_before = datetime.datetime.fromtimestamp(before)
    print( interval, " : 처음" , date_before, "현재", date_now  )
    if 'd' in interval : 
        day_rest = date_now.minute % int(interval.replace('d',''))
        date_now = date_now - datetime.timedelta(days=day_rest) 
        print(date_now.day , date_before.day )
        if date_now > date_before and ( date_now.day > date_before.day ) :
            print("save new Data")
            return True 
    elif 'h' in interval :
        hours_rest = date_now.minute % int(interval.replace('h',''))
        date_now = date_now - datetime.timedelta(hours=hours_rest) 
        print(date_now.hour , date_before.hour )
        if date_now > date_before and ( date_now.day > date_before.day or date_now.hour > date_before.hour) :
            print("save new Data")
            return True 
    else :
        return False

class candle_worker(QThread):
    dataSent = pyqtSignal(list)
    def __init__(self, interval):
        super().__init__()
        self.alive = True
        self.interval = interval

    def run(self):
        if self.interval == '1d' :
            before  = time.time() - 86400
        elif self.interval == '4h' :
            before  = time.time() - 3600*4
        elif self.interval == '8h' :
            before  = time.time() - 3600*8
        while self.alive :
            now     = time.time()
            if time_checker( interval = self.interval, before = before, now=now) :
                before = now
                data = check_candle_data( self.interval, limit = '90' )
                self.dataSent.emit(data)
            time.sleep(7200)

    def stop(self):
        self.alive = False
        self.quit()
        
class volume_worker(QThread):
    dataSent = pyqtSignal(list)
    def __init__(self, interval):
        super().__init__()
        self.alive = True
        self.interval = interval

    def run(self):
        if self.interval == '1d' :
            before  = time.time() - 86400
        elif self.interval == '4h' :
            before  = time.time() - 3600*4
        elif self.interval == '8h' :
            before  = time.time() - 3600*8
        while self.alive :
            now     = time.time()
            # if time_checker( interval = self.interval, before = before, now=now) :
            before = now
            ticker = list(marketlist_all.keys())
            gateio_dt = Accumerate_data(ticker=ticker, interval= self.interval )
            gateio_dt.start()
            data = check_volume_data( self.interval, limit = '90' )
            self.dataSent.emit(data)
            time.sleep(7200)

    def stop(self):
        self.alive = False
        self.quit()
        
# orderbook_0.py
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import time
import os 
from CreonAPI import Client
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('__file__')))) #상위 경로 추가 
from util.binance_coin import *
from Dataloader.RT_data import *

def check_data( interval, limit = '104' ) :
    # self.CallTeleBot( text = "<--{}시작------------->".format(interval))
    # self.CallTeleBot( text= str(datetime.datetime.now()) )
    up_coin = []
    down_coin = []
    list_coin = []
    for _coin in Market_Coin :
        coin_data = load_sql_data(_coin, interval, limit = limit)
        last = coin_data.iloc[0]
        max_data = coin_data.sort_values(ascending = False, by = 'close').iloc[:5]
        min_data = coin_data.sort_values(ascending = True , by = 'close').iloc[:5]
        trader_data = coin_data.sort_values(ascending = False, by = 'QuoteAssetVolume').iloc[:5]

        if  last['date'] in max_data.date.values :
            index_num = max_data.date.values.tolist().index(last['date'])
            middle = ( max_data.iloc[0]['close'] + min_data.iloc[0]['close'] ) / 2  
            up_percent = round( (last['close']/min_data.iloc[0]['close'] - 1) * 100, 1 )
            middle_percent = round( (  middle/min_data.iloc[0]['close'] - 1) * 100, 1 )
            # up_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, up_percent, middle_percent ])
            append_data = {
                'coin' : _coin,
                'close': last['close'],
                'highprice' : max_data.iloc[0]['close'],
                'lowprice' : min_data.iloc[0]['close'],
                'middle' : middle,
                'diffrent' : up_percent,
                'mid_differnt' : middle_percent,
                'index_num' : index_num
            } 
            # list_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, up_percent, middle_percent ])
            list_coin.append(append_data)
            # txt = " {} 코인 {} {} 3순위 <높은> 종가 {} ".format( _coin, interval, limit, round(coin_data['close'].iloc[0], 7) )
            # self.CallTeleBot( text = txt)

        elif last['date'] in min_data.date.values :
            index_num = min_data.date.values.tolist().index(last['date'])
            middle = ( max_data.iloc[0]['close'] + min_data.iloc[0]['close'] ) / 2  
            down_percent = round( ( last['close']/max_data.iloc[0]['close'] - 1) * 100, 1 )
            middle_percent = round( ( middle/max_data.iloc[0]['close'] - 1) * 100, 1 )
            append_data = {
                'coin' : _coin,
                'close': last['close'],
                'highprice' : max_data.iloc[0]['close'],
                'lowprice' : min_data.iloc[0]['close'],
                'middle' : middle,
                'diffrent' : down_percent,
                'mid_differnt' : middle_percent,
                'index_num' : index_num
            } 
            # down_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, down_percent, middle_percent ])
            # list_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, down_percent, middle_percent ])
            list_coin.append(append_data)
            # txt = " {} 코인 {} {} 3순위 <낮은> 종가 {} ".format( _coin, interval, limit, round(coin_data['close'].iloc[0], 7) )
            # self.CallTeleBot( text = txt)

        elif  last['date'] in trader_data.date.values :
            index_num = trader_data.date.values.tolist().index(last['date'])
            middle = ( trader_data.iloc[0]['close'] + min_data.iloc[0]['close'] ) / 2  
            up_percent = round( (last['close']/min_data.iloc[0]['close'] - 1) * 100, 1 )
            middle_percent = round( (  last['close']/max_data.iloc[0]['close'] - 1) * 100, 1 )
            # up_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, up_percent, middle_percent ])
            append_data = {
                'coin' : _coin + '거래량',
                'close': last['close'],
                'highprice' : max_data.iloc[0]['close'],
                'lowprice' : min_data.iloc[0]['close'],
                'middle' : middle,
                'diffrent' : up_percent,
                'mid_differnt' : middle_percent,
                'index_num' : index_num
            } 
            # list_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, up_percent, middle_percent ])
            list_coin.append(append_data)
            # txt = " {} 코인 {} {} 3순위 <높은> 종가 {} ".format( _coin, interval, limit, round(coin_data['close'].iloc[0], 7) )
            # self.CallTeleBot( text = txt)
    return list_coin

def whole_check_data( interval, limit = '104' ) :
    # self.CallTeleBot( text = "<--{}시작------------->".format(interval))
    # self.CallTeleBot( text= str(datetime.datetime.now()) )
    up_coin = []
    down_coin = []
    list_coin = []
    for _coin in Market_Coin :
        coin_data = load_sql_data(_coin, interval, limit = limit)
        last = coin_data.iloc[0]
        max_data = coin_data.sort_values(ascending = False, by = 'close').iloc[:5]
        min_data = coin_data.sort_values(ascending = True , by = 'close').iloc[:5]
        trader_data = coin_data.sort_values(ascending = False, by = 'QuoteAssetVolume').iloc[:5]

        if  last['date'] in max_data.date.values :
            more_data = load_sql_data(_coin, interval, limit = str( int(limit) * 4 ) )
            more_max_data = more_data.sort_values(ascending = False, by = 'close').iloc[0]
            more_min_data = more_data.sort_values(ascending = True , by = 'close').iloc[0]
            index_num = max_data.date.values.tolist().index(last['date'])
            middle = ( max_data.iloc[0]['close'] + min_data.iloc[0]['close'] ) / 2  
            up_percent = round( (last['close']/min_data.iloc[0]['close'] - 1) * 100, 1 )
            middle_percent = round( (  middle/min_data.iloc[0]['close'] - 1) * 100, 1 )
            more_up_percent = round( (last['close']/more_min_data['close'] - 1) * 100, 1 )
            more_down_percent = round( (  last['close']/more_max_data['close'] - 1) * 100, 1 )
            # up_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, up_percent, middle_percent ])
            append_data = {
                'coin' : _coin,
                'close': last['close'],
                'highprice' : max_data.iloc[0]['close'],
                'lowprice' : min_data.iloc[0]['close'],
                'middle' : middle,
                'diffrent' : up_percent,
                # 'mid_differnt' : middle_percent,
                'more_up_percent' : more_up_percent,
                'more_down_percent' : more_down_percent,
                'index_num' : index_num
            } 
            # list_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, up_percent, middle_percent ])
            list_coin.append(append_data)
            # txt = " {} 코인 {} {} 3순위 <높은> 종가 {} ".format( _coin, interval, limit, round(coin_data['close'].iloc[0], 7) )
            # self.CallTeleBot( text = txt)

        elif last['date'] in min_data.date.values :
            more_data = load_sql_data(_coin, interval, limit = str( int(limit) * 4 ))
            more_max_data = more_data.sort_values(ascending = False, by = 'close').iloc[0]
            more_min_data = more_data.sort_values(ascending = True , by = 'close').iloc[0]
            index_num = min_data.date.values.tolist().index(last['date'])
            middle = ( max_data.iloc[0]['close'] + min_data.iloc[0]['close'] ) / 2  
            down_percent = round( ( last['close']/max_data.iloc[0]['close'] - 1) * 100, 1 )
            middle_percent = round( ( middle/max_data.iloc[0]['close'] - 1) * 100, 1 )
            more_up_percent = round( (last['close']/more_min_data['close'] - 1) * 100, 1 )
            more_down_percent = round( (  last['close']/more_max_data['close'] - 1) * 100, 1 )
            append_data = {
                'coin' : _coin,
                'close': last['close'],
                'highprice' : max_data.iloc[0]['close'],
                'lowprice' : min_data.iloc[0]['close'],
                'middle' : middle,
                'diffrent' : down_percent,
                # 'mid_differnt' : middle_percent,
                'more_up_percent' : more_up_percent,
                'more_down_percent' : more_down_percent,
                'index_num' : index_num
            } 
            # down_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, down_percent, middle_percent ])
            # list_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, down_percent, middle_percent ])
            list_coin.append(append_data)
            # txt = " {} 코인 {} {} 3순위 <낮은> 종가 {} ".format( _coin, interval, limit, round(coin_data['close'].iloc[0], 7) )
            # self.CallTeleBot( text = txt)

        elif  last['date'] in trader_data.date.values :
            more_data = load_sql_data(_coin, interval, limit = str( int(limit) * 4 ))
            more_max_data = more_data.sort_values(ascending = False, by = 'close').iloc[0]
            more_min_data = more_data.sort_values(ascending = True , by = 'close').iloc[0]
            index_num = trader_data.date.values.tolist().index(last['date'])
            middle = ( trader_data.iloc[0]['close'] + min_data.iloc[0]['close'] ) / 2  
            up_percent = round( (last['close']/min_data.iloc[0]['close'] - 1) * 100, 1 )
            middle_percent = round( (  last['close']/max_data.iloc[0]['close'] - 1) * 100, 1 )
            more_up_percent = round( (last['close']/more_min_data['close'] - 1) * 100, 1 )
            more_down_percent = round( (  last['close']/more_max_data['close'] - 1) * 100, 1 )
            # up_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, up_percent, middle_percent ])
            append_data = {
                'coin' : _coin + '거래량',
                'close': last['close'],
                'highprice' : max_data.iloc[0]['close'],
                'lowprice' : min_data.iloc[0]['close'],
                'middle' : middle,
                'diffrent' : up_percent,
                # 'mid_differnt' : middle_percent,
                'more_up_percent' : more_up_percent,
                'more_down_percent' : more_down_percent,
                'index_num' : index_num
            } 
            # list_coin.append([ _coin, last['close'], max_data.iloc[0]['close'], min_data.iloc[0]['close'],  middle, up_percent, middle_percent ])
            list_coin.append(append_data)
            # txt = " {} 코인 {} {} 3순위 <높은> 종가 {} ".format( _coin, interval, limit, round(coin_data['close'].iloc[0], 7) )
            # self.CallTeleBot( text = txt)
    return list_coin

def time_checker(interval, before, now) :
    date_now = datetime.datetime.fromtimestamp(now) 
    date_before = datetime.datetime.fromtimestamp(before)
    print( interval, " : 처음" , date_before, "현재", date_now  )
    if 'm' in interval : 
        minutes_rest = date_now.minute % int(interval.replace('m',''))
        date_now = date_now - datetime.timedelta(minutes=minutes_rest) 
        print(date_now.minute , date_before.minute )
        if date_now > date_before and ( date_now.day > date_before.day or date_now.minute > date_before.minute or date_now.hour > date_before.hour) :
            print("save new Data")
            return True 
    # if 'm' in interval : 
    #     multi_int = int ( 60 / int(interval.replace('m','')) )
    #     date_now     = datetime.datetime.fromtimestamp ( time.mktime(date_now.timetuple()) * multi_int )
    #     date_before  = datetime.datetime.fromtimestamp ( time.mktime(date_before.timetuple()) * multi_int )
    # if date_now.hour != date_before.hour :
    #     return True 
    else :
        return False

class min5worker(QThread):
    dataSent = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.binance_api = Client.instance()
        self.alive = True
        self.interval = '1m'
        self.load_data_api  = trade_data( target_coin = Market_Coin, interval = self.interval )

    def run(self):
        before  = time.time() - 200
        while self.alive :
            now     = time.time()
            if time_checker( interval = self.interval, before = before, now=now) :
                before = now
                self.load_data_api.start()
                # data = check_data( interval = self.interval, limit = '156' )
                data = whole_check_data( interval = self.interval, limit = '156' )
                self.dataSent.emit(data)
            time.sleep(20)

    def stop(self):
        self.alive = False
        self.quit()
    
class min15worker(QThread):
    dataSent = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.binance_api = Client.instance()
        self.alive = True
        self.interval = '1m'
        # self.load_data_api  = trade_data( target_coin = Market_Coin, interval = self.interval )

    def run(self):
        before  = time.time() - 200
        while self.alive :
            now     = time.time()
            if time_checker( interval = self.interval, before = before, now=now) :
                before = now
                # data = check_data( interval = self.interval, limit = '624' )
                data = whole_check_data( interval = self.interval, limit = '624' )
                self.dataSent.emit(data)
            time.sleep(20)

    def stop(self):
        self.alive = False
        self.quit()


class min30worker(QThread):
    dataSent = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.binance_api = Client.instance()
        self.alive = True
        self.interval = '3m'
        self.load_data_api  = trade_data( target_coin = Market_Coin, interval = self.interval )

    def run(self):
        before  = time.time() - 200
        while self.alive :
            now     = time.time()
            if time_checker( interval = self.interval, before = before, now=now) :
                before = now
                self.load_data_api.start()
                # data = check_data( interval = self.interval, limit = '624' )
                data = whole_check_data( interval = self.interval, limit = '624' )
                self.dataSent.emit(data)
            time.sleep(30)

    def stop(self):
        self.alive = False
        self.quit()

class hourworker(QThread):
    dataSent = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.binance_api = Client.instance()
        self.alive = True
        self.interval = '3m'
        
    def run(self):
        before  = time.time() - 200
        while self.alive :
            now     = time.time()
            if time_checker( interval = self.interval, before = before, now=now) :
                before = now
                # data = check_data( interval = self.interval, limit = '1248' )
                data = whole_check_data( interval = self.interval, limit = '1248' )
                self.dataSent.emit(data)
            time.sleep(30)

    def stop(self):
        self.alive = False
        self.quit()

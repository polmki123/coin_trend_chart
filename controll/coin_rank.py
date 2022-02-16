# orderbook_0.py
import enum
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtChart import * 
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import os 

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from gate_api import ApiClient, Configuration, Loan, MarginApi, Order, RepayRequest, SpotApi, Transfer, WalletApi
from gate_api.exceptions import GateApiException

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('__file__')))) #상위 경로 추가 

from model.process import * 
from model.coinmarketcap import *

class CoinRankWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        path = os.path.abspath(os.path.dirname(__file__))
        uic.loadUi( os.path.join (path, "../gui/coin_rank.ui"), self)
        
    def color_change(self, component, checking) :
        if float(checking) > 0 :
            component.setForeground(QBrush(Qt.green))
        else :
            component.setForeground(QBrush(Qt.red))
            
    # 'ask_price': 829.0, 'bid_price': 800.0, 'ask_size': 3588.0, 'bid_size': 26999.103125
    def updateData(self, data):
        print( len(data) )
        
        all_coin = []
        for _data in data :
            all_coin.append(_data['coin'])
            
        coin_info = checkAPI_info( [ coin_cap_id[key] for key in all_coin ] )
        
        tag_word = {}
        tag_set = {}
        for _coin in all_coin :
            tag = coin_info['data'][str(coin_cap_id[_coin])]['tag-names']
            tag_word[_coin] = tag
            
            if tag is not None :
                for _t in tag : 
                    if _t not in tag_set.keys():
                        tag_set[_t] = [ _coin ] 
                    else :
                        tag_set[_t].append(_coin)

        self.rank_table.setRowCount(len(tag_set)*3)
        self.rank_table.setColumnCount( len( tag_set[ max( tag_set, key= lambda x : len(set(tag_set[x])) ) ] ))
        # data = sorted ( data, key = ( lambda x : float(x['quotevolume']) ) , reverse = True )  
        print(self.rank_table.rowCount())
        
        tag_sort = sorted(tag_set.items(), reverse=True, key=lambda x: len(set(x[1])) )

        for i, _tag_sort  in enumerate(tag_sort):
            _tag_name = _tag_sort[0]
            item_0 = QTableWidgetItem(f"{ _tag_name }")
            tag = i + i*2
            self.rank_table.setItem(tag, 0, item_0)
            self.rank_table.setSpan(tag, 0, 3, 1)
            
            row_data = [] 
            
            for j, _data in enumerate(data) :
                if _data['coin']  in tag_set[ _tag_name ] :
                    row_data.append( [ _data['coin'], _data['data'].iloc[-1].close, _data['data'].iloc[-1].change  ])
            row_data.sort(key=lambda x:x[2], reverse=True )
                # print(_data['coin'] , _data['data'])
            for j in range( 0, len(row_data) ) :
                self.rank_table.setItem(tag, j + 1, QTableWidgetItem(f"{row_data[j][0]}"))
                self.rank_table.setItem(tag + 1, j + 1, QTableWidgetItem( f"{float(row_data[j][1])}") )
                tmp_item = QTableWidgetItem(f"{float(row_data[j][2]):.2f}")
                self.color_change(tmp_item, row_data[j][2])
                self.rank_table.setItem(tag + 2, j + 1, tmp_item )
               


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    rw = CurrentPriceWidget()
    rw.show()
    exit(app.exec_())
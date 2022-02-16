# orderbook_0.py
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

class CoinInfoWidget(QWidget):
    
    def __init__(self, parent=None):
        
        super().__init__(parent)
        path = os.path.abspath(os.path.dirname(__file__))
        uic.loadUi( os.path.join (path, "../gui/coininfo.ui"), self)
        self.graph_layout_tag = QVBoxLayout(self.coin_tag) # UI로 생성한 위젯을 레이아웃으로 설정
        self.graph_layout_rank = QVBoxLayout(self.coin_trend) # UI로 생성한 위젯을 레이아웃으로 설정
        
    # 'ask_price': 829.0, 'bid_price': 800.0, 'ask_size': 3588.0, 'bid_size': 26999.103125
    def updateData(self, data):
        
        print( len(data) )
        
        # 각 코인 별 tag Layout
        formLayout_tag = QFormLayout()
        groupBox_tag = QGroupBox()
        
        # 전체 tag Layout
        formLayout_rank = QFormLayout()
        groupBox_rank = QGroupBox()
        
        all_coin = []
        for _data in data :
            all_coin.append(_data['coin'])
            
        coin_info = checkAPI_info( [ coin_cap_id[key] for key in all_coin ] )
        
        word = {}
        
        for key in all_coin :
            tag = coin_info['data'][str(coin_cap_id[key])]['tags']
            # print(key, tag)
            
            # 각 태그별 언어 저장 진행 
            if tag is not None :
                for _t in tag : 
                    if _t not in word.keys():
                        word[_t] = 1 
                    else :
                        word[_t] += 1 
                
            formLayout_tag.addRow( QLabel (key) )
            formLayout_tag.addRow( QLabel ( ' '.join(tag) if tag  else "아직 특정된 tag 없음") )
            
        # form Layout을 활용한 groupBox
        groupBox_tag.setLayout(formLayout_tag)

        # Scorll Area 추가로 내려감 
        scroll_tag = QScrollArea()
        scroll_tag.setWidget(groupBox_tag)
        scroll_tag.setWidgetResizable(True)

        # 우선 코인 태그 먼저 표시 
        self.graph_layout_tag.addWidget(scroll_tag)
        
        # 이제 코인 전체 추의 표시 
        pgm_lang_val_reverse = sorted(word.items(), reverse=True, key=lambda item: item[1])
        for key, value in pgm_lang_val_reverse:
            print(key, ":", value)
            formLayout_rank.addRow( QLabel( key + ":" ) , QLabel (str(value)) )
            
        groupBox_rank.setLayout(formLayout_rank)
        
        # Scorll Area 추가로 내려감 
        scroll_rank = QScrollArea()
        scroll_rank.setWidget(groupBox_rank)
        scroll_rank.setWidgetResizable(True)

        # 우선 코인 태그 먼저 표시 
        self.graph_layout_rank.addWidget(scroll_rank)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    rw = CurrentPriceWidget()
    rw.show()
    exit(app.exec_())
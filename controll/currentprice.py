# orderbook_0.py
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import os 
from gate_api import ApiClient, Configuration, Loan, MarginApi, Order, RepayRequest, SpotApi, Transfer, WalletApi
from gate_api.exceptions import GateApiException

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('__file__')))) #상위 경로 추가 

from model.process import * 

class Price1dWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        path = os.path.abspath(os.path.dirname(__file__))
        uic.loadUi( os.path.join (path, "../gui/currentprice.ui"), self)
        self.rw = volume_worker(interval = '1d')

    def StartData(self) :
        try :
            self.rw.stop()
        except :
            print("no worker")
        time.sleep(1)
        self.rw = volume_worker(interval = '1d')
        self.rw.dataSent.connect(self.updateData)
        self.rw.start()

    def StopData(self) :
        self.rw.stop()
        
    def closeEvent(self, event):
        self.rw.close()

    def color_change(self, component, checking) :
        if float(checking) > 0 :
            component.setForeground(QBrush(Qt.green))
        else :
            component.setForeground(QBrush(Qt.red))

    # 'ask_price': 829.0, 'bid_price': 800.0, 'ask_size': 3588.0, 'bid_size': 26999.103125
    def updateData(self, data):
        print(len(data) )
        self.realprice_table.setRowCount(len(data)*3)
        self.realprice_table.setColumnCount(8)
        # data = sorted ( data, key = ( lambda x : float(x['quotevolume']) ) , reverse = True )
        print(self.realprice_table.rowCount())
        for _data in data :
            if len(_data['data']) > 7 :
                date = _data['data'].iloc[-7:]
                for i, _date in enumerate(date.date) :
                    self.realprice_table.setHorizontalHeaderItem( i + 1, QTableWidgetItem(_date) )
                break
            
        for i, _data in enumerate(data):
            # 같은 데이터의 memory를 공유함으로 따로 변수를 만들어서 사용 
            
            ck_data = _data['data'].iloc[-7:] if len(_data['data'] ) > 7 else _data['data']
                
            item_0 = QTableWidgetItem(f"{_data['coin']}")
            tag = i + i*2
            self.realprice_table.setItem(tag, 0, item_0)
            self.realprice_table.setSpan(tag, 0, 3, 1)
            # print(_data['coin'] , _data['data'])
            for j in range( 0, len(ck_data) ) :
                # item_1 = QTableWidgetItem(f"{_data.iloc[j].close}").setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                # item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.realprice_table.setItem(tag, 7 - j , QTableWidgetItem(f"{float(ck_data.iloc[ -1 - j].close):.7f}"))
                # item_1 = QTableWidgetItem(f"{_data.iloc[j].close}")
                # item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                tmp_item = QTableWidgetItem(f"{float(ck_data.iloc[-1 - j].change):.2f}")
                self.color_change(tmp_item, ck_data.iloc[-1 - j].change)
                self.realprice_table.setItem(tag + 1, 7 - j, tmp_item )
                # item_1 = QTableWidgetItem(f"{float(_data.iloc[j].volume):.0f}")
                # item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.realprice_table.setItem(tag + 2, 7 - j, QTableWidgetItem( f"{float(ck_data.iloc[-1 - j].volume)*float( ( ck_data.iloc[-1 - j].high + ck_data.iloc[-1 - j].low) / 2 ):,.0f}") )
                # self.realprice_table.setItem(tag + 2, 7 - j, QTableWidgetItem( f"{float(_data['data'].iloc[-1 - j].volume)*float(_data['data'].iloc[-1 - j].close):,.0f}") )


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    rw = CurrentPriceWidget()
    rw.show()
    exit(app.exec_())
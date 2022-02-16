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

from mpl_finance import candlestick_ohlc

from gate_api import ApiClient, Configuration, Loan, MarginApi, Order, RepayRequest, SpotApi, Transfer, WalletApi
from gate_api.exceptions import GateApiException
from pandas import Series

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('__file__')))) #상위 경로 추가 

from model.process import * 

plt.rcParams.update({'figure.max_open_warning': 0})

class CandleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        path = os.path.abspath(os.path.dirname(__file__))
        uic.loadUi( os.path.join (path, "../gui/candlechart.ui"), self)
        self.rw = candle_worker(interval = '1d')
        # 전체 layout 
        self.graph_layout = QVBoxLayout(self.coin_graphs) # UI로 생성한 위젯을 레이아웃으로 설정
        
    def StartData(self) :
        try :
            self.rw.stop()
        except :
            print("no worker")
        time.sleep(1)
        self.rw = candle_worker(interval = '1d')
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

    def updateData(self, data):
        # for _data in data :
        formLayout = QFormLayout()
        groupBox = QGroupBox()
        
        # 코인 별 데이터 설정 및 formLayout에 추가 진행 
        for i in range(len(data)) :
            print( data[i]['coin'])
            _chart =  CoinChart(data[i]['data']) #FigureCanvas(Figure(figsize=(5, 3)))
            labelA =  QLabel(data[i]['coin'])
            # 각각의 formLayout
            formLayout.addRow(labelA)
            formLayout.addRow(_chart)

        # form Layout을 활용한 groupBox
        groupBox.setLayout(formLayout)

        # Scorll Area 추가로 내려감 
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        self.graph_layout.addWidget(scroll)
        

# 코인 차트를 그린다. 
class CoinChart(FigureCanvas):
    def __init__(self, data, parent=None, width=5, height=4, dpi=100):
        self.graph_init(parent)
        self.data_init(data)
        self.plot(data)
        self.cnt = 99
        
    # 데이터 초기 설정 진행 
    def data_init(self, data):
        self.df = data
        self.x = np.arange(len(self.df.index))
        self.ohlc = self.df[['open', 'high', 'low', 'close']].values
        self.dohlc = np.hstack((np.reshape(self.x, (-1, 1)), self.ohlc))

        self._xticks = []
        self._xlabels = []
        
        # _wd_prev = 0
        # # 일주일 마다 분류하기위한 날짜 표시를 하기 위한 세팅 
        # for _x, d in zip(self.x, self.df.date.values):
        #     weekday = datetime.datetime.strptime(str(d), '%m-%d').month()
        #     if weekday <= _wd_prev:
        #         self._xticks.append(_x)
        #         self._xlabels.append(datetime.datetime.strptime(str(d), '%m-%d').strftime('%m/%d'))
        #     _wd_prev = weekday

        _wd_prev = 1
        # 달마다 표시하기 위한 날짜 세팅 
        for _x, d in zip(self.x, self.df.date.values):
            first_day = datetime.datetime.strptime(str(d), '%m-%d').day
            if first_day <= _wd_prev:
                self._xticks.append(_x)
                self._xlabels.append(datetime.datetime.strptime(str(d), '%m-%d').strftime('%m/%d'))
            _wd_prev = first_day
            
    # 그래프를 그려주는 곳 
    def graph_init(self, parent):
        fig = plt.figure(figsize=(6, 4)) 
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
        self.axes = []
        self.axes.append(plt.subplot(gs[0]))
        self.axes.append(plt.subplot(gs[1], sharex=self.axes[0]))
        self.axes[0].get_xaxis().set_visible(False)
        
        FigureCanvas.__init__(self, fig)
        
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                    QSizePolicy.Expanding,
                                    QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)

    def plot(self, coin):
        # 데이터 바인딩
        #   axes[0]: 캔들 차트
        #   axes[1]: 주문량
        
        # 이동 평균선 그리기 
        self.df['MA5'] = self.df['close'].rolling(5).mean()
        self.df['MA20'] = self.df['close'].rolling(20).mean()
        self.df['MA60'] = self.df['close'].rolling(60).mean()

        self.axes[0].plot(self.x, self.df['MA5'], label='MA5', linewidth=0.7)
        self.axes[0].plot(self.x, self.df['MA20'], label='MA20', linewidth=0.7)
        self.axes[0].plot(self.x, self.df['MA60'], label='MA60', linewidth=0.7)
        
        candlestick_ohlc(self.axes[0], self.dohlc, width=0.5, colorup='r', colordown='b')
        color_fuc = lambda x : 'r' if x >= 0 else 'b'
        color_list  = list(self.df['close'].diff().fillna(0).apply(color_fuc))
        self.axes[1].bar(self.x, self.df.volume, color=color_list, width=0.6, align='center')
        
        # x축 데이터 바인딩
        self.axes[1].set_xticks(self._xticks)
        self.axes[1].set_xticklabels(self._xlabels, rotation=45, minor=False)

        # plt.tight_layout()
        self.draw()
    
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    rw = CurrentPriceWidget()
    rw.show()
    exit(app.exec_())
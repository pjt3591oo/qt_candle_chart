import sys, random

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from mpl_finance import candlestick_ohlc

import pandas as pd
import numpy as np
import datetime
from datetime import timedelta

from upbit import Upbit

form_class = uic.loadUiType("main.ui")[0]

class App(QMainWindow, form_class):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.initUI()
    self.show()
    
    self.upbit = Upbit()
    self.upbit.update_signal.connect(self.update)
    
    self.upbit.start() # 해당 쓰레드의 run 메서드 호출 

  def initUI(self):
    
    self.BTC_chart =  CoinChart("BTC") #FigureCanvas(Figure(figsize=(5, 3)))
    self.EOS_chart = CoinChart("EOS")  #FigureCanvas(Figure(figsize=(5, 3)))
    self.ETH_chart = CoinChart("ETH")  #FigureCanvas(Figure(figsize=(5, 3)))
    
    graph_layout = QVBoxLayout(self.coin_graphs) # UI로 생성한 위젯을 레이아웃으로 설정
    graph_layout.addWidget(self.BTC_chart)
    graph_layout.addWidget(self.EOS_chart)
    graph_layout.addWidget(self.ETH_chart)

  @pyqtSlot(dict)
  def update(self, data):
    code = data['code'].split('-')[1]
    if code == "BTC": 
      self.BTC_chart.updateData(data)
    elif code == "EOS": 
      self.EOS_chart.updateData(data)
    elif code == "ETH": 
      self.ETH_chart.updateData(data)

class CoinChart(FigureCanvas):
  def __init__(self, coin, parent=None, width=5, height=4, dpi=100):
    self.graph_init(parent)
    self.data_init(coin)
    self.plot(coin)
    self.cnt = 99
  def updateData(self, data):
    code = data['code'].split('-')[1]
    self.cnt += 1
    print(code, self.cnt)
    last_dt = datetime.datetime.strptime(self.df['date'].iloc[-1], "%Y%m%d")
    delta_dt = timedelta(days=1)
    new_date = last_dt+ delta_dt
    receive_df = pd.DataFrame({
      "close":[ data['trade_price']],
      "high": [ data['high_price']],
      "low":  [data['low_price']],
      "open": [data['opening_price']],
      "volume":[data['trade_volume']],
      "date": [new_date.strftime('%Y%m%d')]
    })
    if self.cnt < 3:
      self.df = pd.concat([self.df[0:-1], receive_df])
    else:
      self.cnt = 0
      self.df = pd.concat([self.df, receive_df])

    self.x = np.arange(len(self.df.index))
    self.ohlc = self.df[['open', 'high', 'low', 'close']].astype(int).values
    self.dohlc = np.hstack((np.reshape(self.x, (-1, 1)), self.ohlc))

    self._xticks = []
    self._xlabels = []
    
    for _x, d in zip(self.x, self.df.date.values):
      self.weekday = datetime.datetime.strptime(str(d), '%Y%m%d').weekday()
      self._xticks.append(_x)
      self._xlabels.append(datetime.datetime.strptime(str(d), '%Y%m%d').strftime('%m/%d'))

    self.plot(code)

  def data_init(self, coin):
    self.df = pd.DataFrame({
      "close":[11155000, 11156000, 11156000, 11148000, 11141000, 11142000, 11145000],
      "high": [11155000, 11156000, 11156000, 11156000, 11146000, 11142000, 11167000],
      "low":  [11153000, 11144000, 11146000, 11146000, 11141000, 11142000, 11137000],
      "open": [11154000, 11156000, 11156000, 11156000, 11146000, 11142000, 11140000],
      "volume": [1.4495, 2.37885, 0.33939, 1.00578, 2.73196, 0.000993, 0.30993],
      "date": ["20200501", "20200502", "20200503", "20200504", "20200505", "20200506", "20200507"]
    })

    self.x = np.arange(len(self.df.index))
    self.ohlc = self.df[['open', 'high', 'low', 'close']].astype(int).values
    self.dohlc = np.hstack((np.reshape(self.x, (-1, 1)), self.ohlc))

    self._xticks = []
    self._xlabels = []

    for _x, d in zip(self.x, self.df.date.values):
      self.weekday = datetime.datetime.strptime(str(d), '%Y%m%d').weekday()
      self._xticks.append(_x)
      self._xlabels.append(datetime.datetime.strptime(str(d), '%Y%m%d').strftime('%m/%d'))

  def graph_init(self, parent):
    fig = plt.figure(figsize=(8, 6)) 
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    self.axes = []
    self.axes.append(plt.subplot(gs[0]))
    self.axes.append(plt.subplot(gs[1], sharex=self.axes[0]))
    self.axes[0].get_xaxis().set_visible(False)

    FigureCanvas.__init__(self, fig)
    
    self.setParent(parent)

    FigureCanvas.setSizePolicy(self,
                                QSizePolicy.Expanding,
                                QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

  def plot(self, coin):
    # 데이터 바인딩
    #   axes[0]: 캔들 차트
    #   axes[1]: 주문량
    candlestick_ohlc(self.axes[0], self.dohlc, width=0.5, colorup='r', colordown='b')
    self.axes[1].bar(self.x, self.df.volume, color='k', width=0.6, align='center')
    
    # x축 데이터 바인딩
    self.axes[1].set_xticks(self._xticks)
    self.axes[1].set_xticklabels(self._xlabels, rotation=0, minor=False)

    plt.tight_layout()
    self.draw()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())

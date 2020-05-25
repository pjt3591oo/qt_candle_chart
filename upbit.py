from PyQt5.QtCore import QThread
from PyQt5 import QtCore

import websocket, json, time
import datetime as pydatetime

try:
    import thread
except ImportError:
    import _thread as thread

def o_m(ws, data):
  print(data)
class Upbit(QThread):
  update_signal = QtCore.pyqtSignal(dict)

  def __init__(self):
    super().__init__()
    
  def run(self):
    ws = websocket.WebSocketApp(
      "wss://api.upbit.com/websocket/v1",
      on_message = lambda ws, msg: self.on_message(ws, msg),
      on_error = lambda ws, msg: self.on_error(ws, msg),
      on_close = lambda ws: self.on_close(ws),
    )
    self.ws = ws
    self.ws.on_open = self.on_open
    self.ws.run_forever()

  def on_message(self, ws, receive_data):
    data = json.loads(receive_data.decode('utf-8'))
    try:
      self.update_signal.emit(data)
    except Exception as err:
      print(err)

  def on_error(self, ws, msg):
    print('error')
    print('error: ', msg)
  
  def on_close(self, ws):
    print('close')

  def on_open(self):
    def run(*args):
      originData = [
        { "ticket": "UNIQUE_TICKET" },
          # { "type": "orderbook", "codes": ["KRW-BTC", "KRW-ETH", "KRW-LTC"], "isOnlyRealtime": True }, 
          { "type": "ticker", "codes": ["KRW-BTC", "KRW-ETH", "KRW-EOS"] }, 
          # { "type": "trade", "codes": ["KRW-BTC", "KRW-ETH", "KRW-LTC"] }
        ]
      self.ws.send(json.dumps(originData))
    thread.start_new_thread(run, ())
    
if __name__ == "__main__":
  upbit = Upbit()
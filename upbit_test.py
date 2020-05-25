import websocket
import json
import datetime as pydatetime


try:
    import thread
except ImportError:
    import _thread as thread

import time

def on_message(ws, message):
    msg = json.loads(message.decode('utf-8'))
    form = "%s [%s %s] %s"%('>'*25, msg['code'], msg['type'], '<'*25)

    if msg['type'] == 'orderbook': # 적색
        form = '\033[31m' + form + '\033[0m'
        msg = "\033[31mtotal_ask_size: %s, total_bid_size: %s, order Unit Count:%s \033[0m"%(msg['total_ask_size'], msg['total_bid_size'], msg['orderbook_units'])
    elif msg['type'] == 'ticker': # 녹색
        form = '\033[32m' + form + '\033[0m'
        msg = "\033[32mopening_price: %s, high_price: %s, low_price: %s, trade_price: %s, prev_closing_price: %s, acc_trade_price: %s, change: %s, change_price: %s, signed_change_price: %s, change_rate: %s, signed_change_rate: %s, ask_bid: %s, trade_volume: %s, acc_trade_volume: %s, trade_date: %s, trade_time: %s, acc_ask_volume: %s, acc_bid_volume: %s, highest_52_week_price: %s, highest_52_week_date: %s, lowest_52_week_price: %s, lowest_52_week_date: %s, trade_status: %s, market_state: %s, market_state_for_ios: %s, is_trading_suspended: %s, delisting_date: %s, market_warning: %s, acc_trade_price_24h: %s, acc_trade_volume_24h: %s \033[0m"%(
            msg["opening_price"],
            msg["high_price"],
            msg["low_price"],
            msg["trade_price"],
            msg["prev_closing_price"],
            msg["acc_trade_price"],
            msg["change"],
            msg["change_price"],
            msg["signed_change_price"],
            msg["change_rate"],
            msg["signed_change_rate"],
            msg["ask_bid"],
            msg["trade_volume"],
            msg["acc_trade_volume"],
            msg["trade_date"],
            msg["trade_time"],
            msg["acc_ask_volume"],
            msg["acc_bid_volume"],
            msg["highest_52_week_price"],
            msg["highest_52_week_date"],
            msg["lowest_52_week_price"],
            msg["lowest_52_week_date"],
            msg["trade_status"],
            msg["market_state"],
            msg["market_state_for_ios"],
            msg["is_trading_suspended"],
            msg["delisting_date"],
            msg["market_warning"],
            msg["acc_trade_price_24h"],
            msg["acc_trade_volume_24h"]
        )
    else: # 황색
        form = '\033[33m' + form + '\033[0m'
        msg = "\033[33mtrade_price: %s, trade_volume: %s, ask_bid: %s, prev_closing_price: %s, change: %s, change_price: %s, sequential_id: %s \033[0m"%(
            msg['trade_price'],
            msg['trade_volume'],
            msg['ask_bid'],
            msg['prev_closing_price'],
            msg['change'],
            msg['change_price'],
            msg['sequential_id']
        )

    print(form, sep='')
    print(msg, sep='')
    print()

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("close")

def on_open(ws):
    def run(*args):
        # https://docs.upbit.com/docs/upbit-quotation-websocket 문서참고
        originData = [
            { "ticket": "UNIQUE_TICKET" },
            # { "type": "orderbook", "codes": ["KRW-BTC", "KRW-ETH", "KRW-LTC"], "isOnlyRealtime": True }, 
            # { "type": "ticker", "codes": ["KRW-BTC", "KRW-ETH", "KRW-LTC"] }, 
            { "type": "trade", "codes": ["KRW-BTC", "KRW-ETH", "KRW-LTC"] }
        ]

        ws.send(json.dumps(originData))

    thread.start_new_thread(run, ())


if __name__ == "__main__":

    ws = websocket.WebSocketApp(
        "wss://api.upbit.com/websocket/v1",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close,
    )
    
    ws.on_open = on_open
    ws.run_forever()
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_finance import candlestick_ohlc

from datetime import timedelta
import pandas as pd
import numpy as np
import datetime, random

import matplotlib.animation as animation

df = pd.DataFrame({
  "close":[11155000, 11156000, 11156000, 11148000, 11141000, 11142000, 11145000],
  "high": [11155000, 11156000, 11156000, 11156000, 11146000, 11142000, 11167000],
  "low":  [11153000, 11144000, 11146000, 11146000, 11141000, 11142000, 11137000],
  "open": [11154000, 11156000, 11156000, 11156000, 11146000, 11142000, 11140000],
  "volume": [1.4495, 2.37885, 0.33939, 1.00578, 2.73196, 0.000993, 0.30993],
  "date": ["20200501", "20200502", "20200503", "20200504", "20200505", "20200506", "20200507"]
})

fig = plt.figure(figsize=(8, 5)) # width, height
fig.set_facecolor('w')
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
axes = []
axes.append(plt.subplot(gs[0]))
axes.append(plt.subplot(gs[1], sharex=axes[0]))
axes[0].get_xaxis().set_visible(False)

x = np.arange(len(df.index))
ohlc = df[['open', 'high', 'low', 'close']].astype(int).values
dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))

# 봉차트
candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')

# 거래량 차트
axes[1].bar(x, df.volume, color='k', width=0.6, align='center')

# x축
_xticks = []
_xlabels = []

for _x, d in zip(x, df.date.values):
    weekday = datetime.datetime.strptime(str(d), '%Y%m%d').weekday()
    _xticks.append(_x)
    _xlabels.append(datetime.datetime.strptime(str(d), '%Y%m%d').strftime('%m/%d'))

axes[1].set_xticks(_xticks)
axes[1].set_xticklabels(_xlabels, rotation=45, minor=False)

print(_xticks)
print(_xlabels)

update_cnt = 0

def update(n):
  global df
  global update_cnt
  global _xticks
  global _xlabels

  if update_cnt == 0:
    update_cnt += 1
    return
  last_dt = datetime.datetime.strptime(df['date'].iloc[-1], "%Y%m%d")
  delta_dt = timedelta(days=1)
  new_date = last_dt+ delta_dt
  
  updated_df = pd.DataFrame({
    "close": [random.randrange(11137000, 11167000, 1)], 
    "high": [random.randrange(11137000, 11167000, 1)] , 
    "low": [random.randrange(11137000, 11167000, 1) ], 
    "open": [random.randrange(11137000, 11167000, 1)] , 
    "volume": [np.random.rand(1)[0] * 10],
    "date": [new_date.strftime('%Y%m%d')]
  })
  print(updated_df)
  df = pd.concat([df, updated_df], axis=0)

  _xlabels.append(new_date.strftime('%m/%d'))
  _xticks.append(len(_xticks))

  x = np.arange(len(df.index))

  ohlc = df[['open', 'high', 'low', 'close']].astype(int).values
  dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))
  
  candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')
  axes[1].bar(x, df.volume, color='k', width=0.6, align='center') 

  axes[1].set_xticks(_xticks)
  axes[1].set_xticklabels(_xlabels, rotation=45, minor=False)

  return fig

ani = animation.FuncAnimation(fig, update, interval=1500)

plt.tight_layout()
plt.show()
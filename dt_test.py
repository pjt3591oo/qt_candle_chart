import pandas as pd
import datetime
from datetime import timedelta

df = pd.DataFrame({
  "close":[11155000, 11156000, 11156000, 11148000, 11141000, 11142000, 11145000],
  "high": [11155000, 11156000, 11156000, 11156000, 11146000, 11142000, 11167000],
  "low":  [11153000, 11144000, 11146000, 11146000, 11141000, 11142000, 11137000],
  "open": [11154000, 11156000, 11156000, 11156000, 11146000, 11142000, 11140000],
  "volume": [1.4495, 2.37885, 0.33939, 1.00578, 2.73196, 0.000993, 0.30993],
  "date": ["20200501", "20200502", "20200503", "20200504", "20200505", "20200506", "20200507"]
})

last_dt = datetime.datetime.strptime(df['date'].iloc[-1], "%Y%m%d")
delta_dt = timedelta(days=1)
print(last_dt)
print(last_dt+ delta_dt)
# datetime.datetime.strptime(str(last_dt+ delta_dt), '%Y%m%d').strftime('%m/%d')
print((last_dt+ delta_dt).strftime('%Y/%m/%d'))
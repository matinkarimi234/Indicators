import finpy_tse as fpy
import pandas as pd

df = pd.DataFrame()
df, df_order_book = fpy.Get_MarketWatch()

out = pd.DataFrame()
out['Ticker'] = df.index
out.to_csv('Tickers.csv')
import finpy_tse as tse
import pandas as pd
import numpy as np

def get_all_names():
    df = tse.Build_Market_StockList(bourse=True,
                                 farabourse=True,
                                 payeh=True,
                                 detailed_list=False,
                                 show_progress=True,
                                 save_excel=False,
                                 save_csv=False)
    return df.index.to_list()

def get_data(stock_num):
    names = get_all_names()
    names = names[:stock_num]
    for i in names:
        print(tse.Get_Price_History(stock=i,
                            start_date='1402-07-01',
                            end_date='1402-07-26',
                            ignore_date=False,
                            adjust_price=True,
                            show_weekday=True,
                            double_date=True))
        
get_data(5)
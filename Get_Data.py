import finpy_tse as tse
import pandas as pd
import numpy as np


# ------ Use once to get the names of stocks -----------
# def get_all_names():
#     df = tse.Build_Market_StockList(bourse=True,
#                                  farabourse=True,
#                                  payeh=True,
#                                  detailed_list=False,
#                                  show_progress=True,
#                                  save_excel=False,
#                                  save_csv=False)
#     df.to_csv('out.csv',encoding='utf-8', index=False)
# get_all_names()


def get_data(stock_num):
    names = pd.read_csv('out.csv')['Name'].to_list()
    names = names[:stock_num]
    df = pd.DataFrame()
    for i in names:
        df1 = pd.DataFrame()
        df1 = tse.Get_Price_History(stock=i,
                                    start_date='1402-07-01',
                                    end_date='1402-07-26',
                                    ignore_date=False,
                                    adjust_price=True,
                                    show_weekday=True,
                                    double_date=True)
    
        df = pd.concat([df,df1],ignore_index=True)
    

    df.to_csv('final.csv',encoding='utf-8', index=False)
        

get_data(5)
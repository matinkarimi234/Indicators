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


def get_data(stock_num,start_date,end_date):
    names = pd.read_csv('out.csv')['Name'].to_list()
    if stock_num == 0:
        stock_num = len(names) - 1
    names = names[:stock_num]
    df = pd.DataFrame()
    for i in names:
        df1 = pd.DataFrame()
        df1 = tse.Get_Price_History(stock=i,
                                    start_date=start_date,
                                    end_date=end_date,
                                    ignore_date=False,
                                    adjust_price=True,
                                    show_weekday=False,
                                    double_date=True)
    
        df = pd.concat([df,df1],ignore_index=True)
    

    df.to_csv('final.csv',encoding='utf-8', index=False)
    return df
import finpy_tse as tse
import pandas as pd
import numpy as np
from persiantools.jdatetime import JalaliDate
import datetime

# ------ Use once to get the names of stocks -----------
# def get_all_names():
#     df = tse.Build_Market_StockList(bourse=True,
#                                  farabourse=True,
#                                  payeh=True,
#                                  detailed_list=True,
#                                  show_progress=True,
#                                  save_excel=False,
#                                  save_csv=False)
#     df.to_csv('out.csv',encoding='utf-8', index=False)
# get_all_names()


def get_data(stock_num = 0 ,days = 5,end_date = JalaliDate.today(),filename='Final.csv'):
    start_date = end_date - datetime.timedelta(days = days)
    names = pd.read_csv('out.csv')['Name'].to_list()
    if stock_num == 0:
        stock_num = len(names) - 1
    names = names[:stock_num]
    df = pd.DataFrame()
    count = 0
    for i in names:
        df1 = pd.DataFrame()
        df1 = tse.Get_Price_History(stock=i,
                                    start_date=str(start_date),
                                    end_date=str(end_date),
                                    ignore_date=False,
                                    adjust_price=True,
                                    show_weekday=False,
                                    double_date=False)
    
        df = pd.concat([df,df1],ignore_index=True)
        count +=1
        print(str(count) + 'out of ' + str(len(names)),flush=True)

    df.to_csv(filename,encoding='utf-8', index=False)

def get_min():
    get_data(days = 30,filename='Monthly.csv')
    df = pd.read_csv('Monthly.csv')
    print(df.index.values.tolist())
get_min()
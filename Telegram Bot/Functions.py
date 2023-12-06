import numpy as np
import pandas as pd
import os
import jdatetime as jd
import finpy_tse as fpy


# MarketWatch Filters
def GetMarketWatch():
    today = jd.date.today().strftime("%Y-%m-%d")
    filename = 'Watch-'+ today + '.csv'
    df = pd.DataFrame()
    if os.path.isfile(filename):
        df =  pd.read_csv(filename)
    else:
        df, df_order_book = fpy.Get_MarketWatch()
        df.to_csv(filename)
    return df


def ascending1(dft = GetMarketWatch()):
    tl = (dft['Day_UL'] - dft['Day_LL'])
    pl = (dft['High'] - dft['Low'])
    cl = (pl - dft['Open'])
    dft = dft.loc[(dft['Close'] > dft['Open']) & (((cl/tl) >= 0.7) | ((pl/tl) >= 0.6))]
    return dft

def ascending2(dft = GetMarketWatch()):
    py = ((dft['Close']*100)/ (dft['Final(%)']+100))
    pc = dft['Final']

    dft = dft.loc[(pc>= py) &(dft['Base-Vol'] < 200000 )& (dft['Final(%)']>=1.5)]

    return dft

def hammer(dft = GetMarketWatch()):
    py = ((dft['Close']*100)/ (dft['Final(%)']+100))
    pc = dft['Final']
    pl = dft['Close']

    pmax = dft['High']
    pmin = dft['Low']
    pf = dft['Open']

    dft = dft.loc[(pl > pc) & (pmax > pmin)]
    if dft.empty == False:

        dft = dft.loc[(pl > pc) & (pmax > pmin) & (pl > py) & (pmax > py)]
        if dft.empty == False:

            dft = dft.loc[(pl > pc) & (pmax > pmin) & (pl > py) & (pmax > py) & (pf >= py) & (pl > pmin)]
            if dft.empty == False:

                dft = dft.loc[(pl > pc) & (pmax > pmin) & (pl > py) & (pmax > py) & (pf >= py) & (pl > pmin) & (pl > pf)]
            else:
                pass
        else:
            pass
    else:
        pass


    return dft


def hammer_ascend1():

    df1 = ascending1()
    
    df_final = pd.DataFrame()
    df_final = hammer(df1)

    return df_final



# Chart Filters


def get_max_year(name):
    today = jd.date.today().strftime("%Y-%m-%d")
    data = fpy.Get_Price_History(stock = name,
                                 start_date = '1402-01-01',
                                 end_date = today,
                                 ignore_date = False,
                                 adjust_price = True,
                                 show_weekday = False,
                                 double_date = False)
    maximum = max(data['Adj Close'])
    return data[data['Adj Close'] == maximum]

def Get_Today_From_99():
    today = jd.date.today().strftime("%Y-%m-%d")
    max_year = pd.DataFrame()
    file_name = 'History-'+ today + '.csv'
    if os.path.isfile(file_name):
        max_year = pd.read_csv(file_name)
    else:
        max_99 = pd.read_csv('max_99.csv')
        count = 1
        for index, row in max_99.iterrows():
            try:
                max_year = pd.concat([max_year,get_max_year(row['Ticker'])], ignore_index = True)
                count+=1
            except:
                count+=1
        max_year.to_csv(file_name)

    return max_year

def Compare_To_99():
    max_99 = pd.read_csv('max_99.csv')
    max_year = Get_Today_From_99()
    result = []
    for index, row in max_99.iterrows():
        try:
            close_99 = np.int64(row['Adj Close'])
            close_year = np.array(max_year[max_year['Ticker'] == row['Ticker']]['Adj Close'])
            if ((close_99 * 2) + close_99) <= close_year[0] :
                result.append(row['Ticker'])
        except Exception as error:
            pass

    res = []
    [res.append(i) for i in result if i not in res]
    return res
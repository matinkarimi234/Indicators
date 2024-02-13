from datetime import timedelta , datetime
import numpy as np
import pandas as pd
import os
import jdatetime as jd
import finpy_tse as fpy
import mplfinance as mpf
import uuid

binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},  
        "edge": {"up": "#3dc985", "down": "#ef4f60"},  
        "wick": {"up": "#3dc985", "down": "#ef4f60"},  
        "ohlc": {"up": "green", "down": "red"},
        "volume": {"up": "#247252", "down": "#82333f"},  
        "vcedge": {"up": "green", "down": "red"},  
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",
}


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
    pl = dft['Close']
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



def P_E(dft = GetMarketWatch()):
    names = []
    for index, row in dft.iterrows():
        if np.float64(row['EPS']) != 0:
            p_e = np.float64(row['Close']) / np.float64(row['EPS'])
            if p_e <= 5:
                names.append(row['Ticker'])
    return names

def hammer_ascend1():

    df1 = ascending1()
    
    # df_final = pd.DataFrame()
    df_final = hammer(df1)

    return df_final

def hammer_ascend2():
    
    df1 = ascending2()
    
    df_final = pd.DataFrame()
    df_final = hammer(df1)

    return df_final

# Chart Filters

def get_max_year(name,start = '1402-01-01'):
    today = jd.date.today().strftime("%Y-%m-%d")
    data = fpy.Get_Price_History(stock = name,
                                 start_date = start,
                                 end_date = today,
                                 ignore_date = False,
                                 adjust_price = True,
                                 show_weekday = False,
                                 double_date = False)
    maximum = max(data['Adj Close'])
    data = data.drop(columns=['Open','High','Low','Close','Final','Volume','Value','No','Name','Market','Adj Open','Adj High','Adj Low','Adj Final'])
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
                print(str(count)+' / '+ str(len(max_99.axes[0])))
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
            if ((close_99 * 1.5) + close_99) <= close_year[0] :
                result.append(row['Ticker'])
        except Exception as error:
            pass

    res = []
    [res.append(i) for i in result if i not in res]
    return res

def Min_Last_Month(name):

    start = (jd.date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
    today = jd.date.today().strftime("%Y-%m-%d")
    today_M = datetime.now().strftime("%Y-%m-%d")
    data = fpy.Get_Price_History(stock = name,
                                 start_date = start,
                                 end_date = today,
                                 ignore_date = False,
                                 adjust_price = True,
                                 show_weekday = False,
                                 double_date = True)
    minimum = min(data['Adj Close'])
    return data[data['Adj Close'] == minimum]

def Min_Month():
    today = jd.date.today().strftime("%Y-%m-%d")
    filename = 'Month-'+ today + '.csv'
    dft = pd.DataFrame()
    if os.path.isfile(filename):
        dft = pd.read_csv(filename)
    else:
        print('Getting Last 3 Months Min...')
        names_99 = Compare_To_99()
        print(names_99)
        names_pe = P_E()
        print('\n')
        print(names_pe)
        print('\n')
        names = list(set(names_99) & set(names_pe))
        print(names)
        count = 0
        with open('names.txt','wb') as f:
            for name in names:
                path = str(uuid.uuid4())
                f.write((name+','+path[0:7]+ '\n' ).encode('utf-8','ignore'))
        for name in names:
            dft = pd.concat([dft,Min_Last_Month(name)], ignore_index = True)
            print(str(count)+' / '+ str(len(names)))
            count +=1
        dft.to_csv(filename)
    return dft

def Get_Each_Data(name,start,end = jd.date.today().strftime("%Y-%m-%d")):
    data = pd.DataFrame()
    data = fpy.Get_Price_History(stock = name,
                                 start_date = start,
                                 end_date = end,
                                 ignore_date = False,
                                 adjust_price = True,
                                 show_weekday = False,
                                 double_date = True)
    return data


def color(goldencrossover):
    UP = []
    DOWN = []
    for i in range(len(goldencrossover)):
        if goldencrossover['Tenkan-sen'][i] < goldencrossover['Kijun-sen'][i]:
            UP.append(float(goldencrossover['Tenkan-sen'][i]))
            DOWN.append(np.nan)
        elif goldencrossover['Tenkan-sen'][i] > goldencrossover['Kijun-sen'][i]:
            DOWN.append(float(goldencrossover['Tenkan-sen'][i]))
            UP.append(np.nan)
        else:
            UP.append(np.nan)
            DOWN.append(np.nan)
    goldencrossover['up'] = UP
    goldencrossover['down'] = DOWN
    return goldencrossover

def golden_cal(df):
    goldenSignal = []
    deathSignal = []
    position = False
    for i in range(len(df)):
        if df['Kijun-sen'][i] > df['Tenkan-sen'][i] and 0.95 < (float(df['Kijun-sen'][i-13])/float(df['Kijun-sen'][i])) < 1.05: # Kijun sen Must be a straight line
            if position == False :
                goldenSignal.append((df['Tenkan-sen'][i]-df['Tenkan-sen'][i]*0.01))
                deathSignal.append(np.nan)
                position = True
            else:
                goldenSignal.append(np.nan)
                deathSignal.append(np.nan)
        elif df['Kijun-sen'][i] < df['Tenkan-sen'][i] and 0.95< (float(df['Tenkan-sen'][i-13])/float(df['Tenkan-sen'][i])) < 1.05: # Tenkan sen Must be a straight line
            if position == True:
                goldenSignal.append(np.nan)
                deathSignal.append((df['Tenkan-sen'][i]+df['Tenkan-sen'][i]*0.01))
                position = False
            else:
                goldenSignal.append(np.nan)
                deathSignal.append(np.nan)
        else:
            goldenSignal.append(np.nan)
            deathSignal.append(np.nan)
    df['GoldenCrossOver'] = goldenSignal
    df['DeathCrossOver'] = deathSignal


def Ichimoku(name,filename):
    start = (jd.date.today() - timedelta(days=800)).strftime("%Y-%m-%d")
    today = jd.date.today().strftime("%Y-%m-%d")
    path = "output\\"+filename+'_'+today+".jpg"
    if os.path.isfile(path):
        pass
    else:
        df = Get_Each_Data(name,start)
        df.reset_index(drop=True,inplace=True)
        df.set_index('Date',inplace=True)


        # Formula To Obtain Ichimoku Cloud 
        df['Tenkan-sen'] = (df['High'].rolling(window=9).max() + df['Low'].rolling(window=9).min()) / 2
        df['Kijun-sen'] = (df['High'].rolling(window=26).max() + df['Low'].rolling(window=26).min()) / 2 
        df['Senkou_Span_A'] = (df['Tenkan-sen'] + df['Kijun-sen']) / 2 
        df['Senkou_Span_B'] = (df['High'].rolling(window=52).max() + df['Low'].rolling(window=52).min()) / 2 
        df['Chikou_Span'] = df['Close'].shift(periods=-26) 

        a = df[['Tenkan-sen']]
        b = df[['Kijun-sen']]
        c = df[['Chikou_Span']]
        d = df[['Senkou_Span_A']]
        e = df[['Senkou_Span_B']]

        golden_cal(df)

        #Fuction Color Applied And Df Generated 
        goldencrossover = color(df)

        up_sma100 = goldencrossover[['up']]
        down_sma100 = goldencrossover[['down']]
        up_sma21 = goldencrossover[['Kijun-sen']]
        gco = goldencrossover[['GoldenCrossOver']]
        dco = goldencrossover[['DeathCrossOver']]


        ic = [
        mpf.make_addplot(a,color='#469ff2',alpha=0.5,label='Tenkan-sen'),
        mpf.make_addplot(b,color='#f26bca',alpha=0.5,label='Kijun-sen'),
        mpf.make_addplot(c,color='#99ff59',alpha=0.8,label='Chikou_Span'),
        mpf.make_addplot(d,color='#006B3D',alpha=0.8,label='Senkou_Span_A'),
        mpf.make_addplot(e,color='#D3212C',alpha=0.8,label='Senkou_Span_B'),
        mpf.make_addplot(gco,type='scatter',markersize=200,marker='v',color='red',panel=0),
        mpf.make_addplot(dco,type='scatter',markersize=200,marker='^',color='green',panel=0),
        ]

        ichimoko_fill_up = dict(y1 = df['Senkou_Span_A'].values, y2 = df['Senkou_Span_B'].values, where = df['Senkou_Span_A'] >= df['Senkou_Span_B'], alpha = 0.5, color = '#a6f7a6')
        ichimoko_fill_down = dict(y1 = df['Senkou_Span_A'].values, y2 = df['Senkou_Span_B'].values, where = df['Senkou_Span_A'] < df['Senkou_Span_B'], alpha = 0.5, color = '#FC8EAC')

        
        mpf.plot(
        df,
        volume=True,
        type="candle",
        title = name,
        fill_between = [ichimoko_fill_up,ichimoko_fill_down],
        style= 'yahoo',
        addplot=ic,
        figsize=(60,30),
        savefig=dict(fname=path,dpi=130,pad_inches=0.25)
        )


def Buy_Queue(dft = GetMarketWatch()):
    pl = dft['Close']
    tmax = dft['Day_UL']

    dft = dft.loc[(pl<tmax) & (pl>=((tmax/100)*99))]

    return dft

def Min_Buy():
    today = jd.date.today().strftime("%Y-%m-%d")
    filename = 'Month-Buy-'+ today + '.csv'
    dft = pd.DataFrame()
    if os.path.isfile(filename):
        dft = pd.read_csv(filename)
    else:
        Buy = Buy_Queue()
        count = 0
        for index, row in Buy.iterrows():
            name = row['Ticker']
            print(str(count) + '/'+str(len(Buy)))
            try:
                minimum = Min_Last_Month(name)
                min_price = np.int64(minimum['Close'])
            
                if min_price < np.int64(row['Close'])< (min_price * 1.1):
                    dft = pd.concat([dft,minimum], ignore_index = True)
                    print('OK!')
            except Exception as error:
                pass
            count+=1

        dft.to_csv(filename)
    return dft

def Base_Volume(dft = GetMarketWatch()):
    bv = np.int64(dft['Base-Vol'])
    volume = np.int64(dft['Volume'])

    dft = dft.loc[ volume >= (bv * 3) ]

    return dft

def Min_Base():
    today = jd.date.today().strftime("%Y-%m-%d")
    filename = 'Month-Base-'+ today + '.csv'

    # Miladi Numpy
    today_M = np.datetime64(datetime.now())
    today_M10 = np.datetime64(datetime.now() - timedelta(days=10))
    
    dft = pd.DataFrame()
    if os.path.isfile(filename):
        dft = pd.read_csv(filename)
    else:
        Base = Base_Volume()
        count = 0
        for index, row in Base.iterrows():
            name = row['Ticker']
            print(str(count) + '/'+str(len(Base)))
            try:
                minimum = Min_Last_Month(name)
                date = minimum['Date'][0]
                if today_M10 <= date <= today_M:
                    dft = pd.concat([dft,minimum], ignore_index = True)
                    print('OK!')
            except Exception as error:
                print(error)
            count+=1

        dft.to_csv(filename)

    return dft



# def Base_Buy():
#     Base = Min_Base()
#     Buy = Min_Buy()
#     Base_names = np.array(Base['Ticker'])
#     Buy_names = np.array(Buy['Ticker'])
#     names = list(set(Base_names) & set(Buy_names))
#     return names


# print(Base_Buy())
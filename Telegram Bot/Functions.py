import pandas as pd
def ascending1(dft = pd.DataFrame()):
    tl = (dft['Day_UL'] - dft['Day_LL'])
    pl = (dft['High'] - dft['Low'])
    cl = (pl - dft['Open'])
    dft = dft.loc[(dft['Close'] > dft['Open']) & (((cl/tl) >= 0.7) | ((pl/tl) >= 0.6))]
    return dft

def ascending2(dft = pd.DataFrame()):
    py = ((dft['Close']*100)/ (dft['Final(%)']+100))
    pc = dft['Final']

    dft = dft.loc[(pc>= py) &(dft['Base-Vol'] < 200000 )& (dft['Final(%)']>=1.5)]

    return dft

def hammer(dft = pd.DataFrame()):
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

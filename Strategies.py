import pandas as pd
import numpy as np
# import finpy_tse as fpy

# df , df_order_book = fpy.Get_MarketWatch()

def hammer(dft = pd.DataFrame()):

    
    
    #P/E
    #dft = dft[((dft['Final'])/(abs(dft['EPS'])) <= 5)]
    
    
#     true == function()
# {
# if((pl) > (pf)) { var tl = (tmax)-(tmin);var pl = (pmax) - (pmin); var cl = (pl) - (pf); if (cl/tl >= 0.7 && pl/tl >= 0.6)
# return true;            
# }
# }
# ()
    tl = (dft['Day_UL'] - dft['Day_LL'])
    pl = (dft['High'] - dft['Low'])
    cl = (pl - dft['Open'])
    dft = dft[(dft['Close'] > dft['Open']) & (((cl/tl) >= 0.7) | ((pl/tl) >= 0.6))]
    

    py = ((dft['Close']*100)/ (dft['Final(%)']+100))
    
    pl = dft['Close']
    pc = dft['Final']
    pmax = dft['High']
    pmin = dft['Low']
    pf = dft['Open']
#     dft = dft[((pl > pc) & (pmax > pmin) & 
#                (pl > py) & (pmax > py) & 
#                (pf >= py) & (pl > pmin) & 
#                (pl > pf) & ((pl/pf) < 1.015) & 
#                ((pl/pf) > 1.005) & (pmax == pf) & ((dft['No']) > 1))]
    
    # (pc) >= (py) && (bvol) < 200000 && (plp) >=1.5

    dft = dft.loc[(pc>= py) &(dft['Base-Vol'] < 200000 )& (dft['Final(%)']>=1.5) & (pl > pc) & (pmax > pmin) & (pl > py) & (pmax > py)]
    
    
    return dft

# df_final = hammer(df)
# print(df_final)


def monthly_min(dft):
    pass
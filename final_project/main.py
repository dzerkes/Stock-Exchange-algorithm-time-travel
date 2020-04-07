# -*- coding: utf-8 -*-
import pandas as pd
from helper import  buy_low , sell_high , decide , write_to_file, update_balance,plot_profit_balance
pd.options.mode.chained_assignment = None 


df = pd.read_csv('mystock.txt',sep=',',index_col=0)
df = df.reset_index()
df = df.drop(labels='index', axis=1)


T = 14
N_max = 100000

datetrack = df.iloc[0]['Date']
lastdate = df.iloc[-1]['Date']  
daterange =  pd.date_range(start=datetrack, periods=T) #period= 365 trexei
#if datetrack in daterange:
#    print('yo')

profit = {'date' :[datetrack],'profit':[1.0]}      # 1$ κερδος
profit = pd.DataFrame.from_dict(profit)

bal  = {'date' :[datetrack],'balance':[1.0]}     # αποτιμηση = κερδος + αξια μετοχων. θα  το υπολογισω στο τελος.
bal = pd.DataFrame.from_dict(bal)

moves_history  = {'date': [], 'move': [], 'stock':[],'Xvolume':[]} 
moves_history  = pd.DataFrame.from_dict(moves_history)

stocks_bought = {'stocks':[] , 'volume':[],'pricepaid':[]} # key is the stock value is the volume
stocks_bought  = pd.DataFrame.from_dict(stocks_bought)





break_flag = False
N = 0
while N <= N_max:
    if str(daterange[-1]).split()[0] > lastdate:
        daterange = lastdate
        break_flag = True

    decision, decision_df = decide(df,profit,stocks_bought,datetrack,daterange)
    if decision_df.empty: # no more moves
        break
    if decision == "sell":
        best_choice = sell_high(decision_df)
        #change profit , stocks_bought , moves_history, datetrack
        datetrack = best_choice['Date']
        
        new_profit = profit['profit'].iloc[-1] + best_choice['earning']
        profit = profit.append({'date' : best_choice['Date'], 'profit':new_profit } ,ignore_index=True)
        
        xvol =  int(best_choice['VolumeToSell'])
       
        
        moves_history = moves_history.append({'date' : best_choice['Date'], 'move':'sell-high','stock':best_choice['Stock'],'Xvolume':xvol} ,ignore_index=True)
        
        i = stocks_bought.index[stocks_bought['stocks'] == best_choice['Stock'] ].tolist()[0]
        stocks_bought.at[i,'volume'] -= xvol
        
        stocks_bought = stocks_bought[stocks_bought.volume != 0] # remove row with that stock cause i sold it.
    
    if decision == "buy": #decision_df comes from to_buy function.
        best_choice = buy_low(decision_df) # best choice to buy
        #now i need to find how much i will buy from that stock!
        #         update datetrack , profit , moves  and , stocks_bought
        datetrack = best_choice['Date']
        if best_choice['Low'] <= 0:
            xvol = int(best_choice['Volume'])
        else:
            xvol = int (profit['profit'].iloc[-1] // best_choice['Low'] )
            if xvol > best_choice['Volume']:
                xvol = int(best_choice['Volume'])
        pricepaid = xvol * best_choice['Low']
        new_profit =  profit['profit'].iloc[-1] - pricepaid
        profit = profit.append({'date' : best_choice['Date'], 'profit':new_profit } ,ignore_index=True)
        
        moves_history = moves_history.append({'date' : best_choice['Date'], 'move':'buy-low','stock':best_choice['Stock'],'Xvolume':xvol} ,ignore_index=True)
        
        if best_choice['Stock'] in stocks_bought.stocks.unique():
            i = stocks_bought.index[stocks_bought['stocks'] == best_choice['Stock'] ].tolist()[0]
            stocks_bought.at[i,'volume'] += xvol
            stocks_bought.at[i,'pricepaid'] = pricepaid
        else:
            stocks_bought = stocks_bought.append({'stocks' : best_choice['Stock'], 'volume':xvol,'pricepaid':pricepaid } ,ignore_index=True)
        
    N += 1 
    print(N ,"----",profit['profit'].iloc[-1],"----")
    ## I SHOULD UPDATE MY BALANCE IN THE END
    balanceSum = update_balance(df,stocks_bought,datetrack, profit['profit'].iloc[-1])
    bal =  bal.append({'date':datetrack, 'balance':balanceSum},ignore_index=True)
    if break_flag == True:
        break;
    
    daterange =  pd.date_range(start=datetrack, periods=T) # πρέπει να επιστρέφω updated datetrack
        
write_to_file(N,moves_history)
plot_profit_balance(profit,bal)





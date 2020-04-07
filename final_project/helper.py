import pandas as pd
import matplotlib.pyplot as plt
#possible buy stocks
def to_buy(df,profit,datetrack,daterange):
    mask = (df['Date'] > datetrack)
    df_buy =  df[mask]
    df_buy = df_buy[df_buy['Date'] <= str(daterange[-1]).split()[0]]
    df_buy = df_buy[df_buy['Low'] <= profit['profit'].iloc[-1]]
    return df_buy

#possible sell stocks
def to_sell(df,stocks_bought,datetrack , daterange):
    if not(stocks_bought.empty):
        mask = (df['Date'] > datetrack) 
        df_sell = df[mask]
        df_sell = df_sell[df_sell['Date'] <= str(daterange[-1]).split()[0]]
        df_sell = df_sell[df_sell['Stock'].isin(list(stocks_bought['stocks'].values))]
        return df_sell
        
    else:       
        return pd.DataFrame()

#decide to sell
def decide(df,profit,stocks_bought,datetrack,daterange):
    df_buy = to_buy(df,profit,datetrack,daterange)
    df_sell = to_sell(df,stocks_bought,datetrack,daterange)
    if df_sell.empty:
        return "buy" , df_buy  

    temp_dfs = []
    #df_sell['difference']= np.nan
    #df_sell['earning']= np.nan
    for stock in list(df_sell.Stock.unique()):
        temp = df_sell.loc[df_sell['Stock'] == stock]
        volume_bought = stocks_bought.loc[stocks_bought['stocks'] == stock]['volume'].values[0] 
        pricepaid = stocks_bought.loc[stocks_bought['stocks'] == stock]['pricepaid'].values[0]
        temp.loc[temp['Volume'] >= volume_bought  , 'VolumeToSell' ] = volume_bought
        temp.loc[temp['Volume'] < volume_bought   , 'VolumeToSell' ] = temp['Volume']
        
        temp['difference'] =  (temp['High'] * temp['VolumeToSell'] )- pricepaid 
        temp['earning'] =  temp['High'] * temp['VolumeToSell']
        temp = temp.loc[temp['difference'] > 0]
        temp_dfs.append(temp)
    result = pd.concat(temp_dfs)
    result = result.sort_values(by =['Date'])
    if result.empty:
        return 'buy' , df_buy
    else:
        return "sell", result
   
def buy_low(dcion_df):
    # get the row of min value in column Low
    dcion_df['variance'] = dcion_df['High'] / dcion_df['Low']
    groupby = dcion_df.groupby(['Stock'])['variance'].mean()
    groupby = groupby.sort_values(ascending=False)
    a = groupby.idxmax() # stock i want!
    stock_interested = dcion_df[dcion_df['Stock'] == a]
    
    return stock_interested.loc[stock_interested['Low'].idxmin()]
 
def sell_high(dcion_df):
    # get the row of max value in column earning
    return dcion_df.loc[dcion_df['difference'].idxmax()]

def update_balance(df,stocks_bought,datetrack, profit):
    balance_sum = profit
    mystocks = list(stocks_bought.stocks.unique()) # oi metoxes pou exw
    myvolume = list(stocks_bought.volume.unique()) # to volume pou exw gia kathe mia apo auti
    myStockVol = zip(mystocks,myvolume)            # tuples (stockName,Volume)
    
    for i,vol in myStockVol:
        #i want the row with stock name = i , and date = datetrack
        myrow = df.loc[(df['Date'] == datetrack) & (df['Stock']== i)]
        if not(myrow.empty):
            close_price = myrow['Close'].values[0]
            balance_sum += vol * close_price
        else:
            continue
                
        
    return  balance_sum
    
def write_to_file(N,moves_history):
    if N<=1000:
        f = open("small.txt", "w")
    else:
        f = open("large.txt", "w")
    f.write(str(N))
    f.write("\n")
    for i in range(len(moves_history)):
        f.write(moves_history.loc[[i]]['date'].values[0])
        f.write(" ")
        f.write(moves_history.loc[[i]]['move'].values[0])
        f.write(" ")
        f.write(moves_history.loc[[i]]['stock'].values[0])
        f.write(" ")
        f.write(str(int(moves_history.loc[[i]]['Xvolume'].values[0])))
        f.write("\n")
    f.close()
    
#plot the diagram of profit and bal through time!
def plot_profit_balance(profit,bal):
    del bal['date']   
    df_merged = pd.concat([profit, bal], axis=1)
    # clean date column from y-m-d to y. !
    df_merged['date'] = pd.DatetimeIndex(df_merged['date']).year
    ax = df_merged.set_index('date').plot(figsize=(10,5), grid=True, kind= 'area',legend=True , stacked=True, title = 'Diagram of my profit and balance')
    ax.margins(0,0)
    plt.show()
    
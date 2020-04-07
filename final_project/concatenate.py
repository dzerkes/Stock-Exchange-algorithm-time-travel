import pandas as pd
import os
os.chdir('cleanstocks')


def stockmerge():
    
    filenames = [x for x in os.listdir() if x.endswith('.txt') and os.path.getsize(x) > 0]
    list_with_df = []
    for file in filenames:
        df = pd.read_csv(file, sep=',')
        df = df.drop(labels='OpenInt', axis=1)
        df['Stock'] = file.split('.')[0]
        df['Volume'] = df['Volume'] * 0.1
        df = df.astype({'Volume': 'int64'})
        list_with_df.append(df)
        
    
    result = pd.concat(list_with_df)
    result = result.sort_values(by =['Date'])
    os.chdir('..')
    result.to_csv('mystock.txt',sep=',')
    
    
stockmerge()      
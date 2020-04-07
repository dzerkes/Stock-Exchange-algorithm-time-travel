import pandas as pd
import os
from collections import OrderedDict
from operator import itemgetter 
from itertools import islice
import shutil

os.chdir('stocks')
filenames = [x for x in os.listdir() if x.endswith('.txt') and os.path.getsize(x) > 0] # all files in Stocks

myScoreDict = {} 

for filename in filenames:
    df = pd.read_csv(filename,sep=',')  
    myScore = df.iloc[-1]['Close'] / df.iloc[0]['Close']
    
    myScoreDict[filename] = myScore

### εχω τα score στο dictionary. Θα κάνω sort και θα παρω τα 200 πρώτα στο φάκελο CleanStocks
n = 5000 # αναλογα ποσα θελω να διαλεξω 
myScoreDict = OrderedDict(sorted(myScoreDict.items(), key = itemgetter(1), reverse = True)) # απο το μεγαλυτερο στο μικροτερο αρα θελω τα πρωτα 200.
myStocks = list(islice(myScoreDict,n)) 

files = os.listdir()

for file in files:
    if file in myStocks:
        full_file_name = os.path.join('', file)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, '../cleanstocks')
        
    
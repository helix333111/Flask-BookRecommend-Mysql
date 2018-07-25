# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 22:26:46 2018

@author: Administrator
"""
import pandas as pd
#清理评分表
path = './data/Ratings1M.csv'
Data = pd.read_csv(path, sep=None)
resultData = pd.DataFrame()
resultData['UserID'] =Data['User-ID,ISBN,Book-Rating'].apply(lambda x: x.split(';')[0])
resultData['BookID'] =Data['User-ID,ISBN,Book-Rating'].apply(lambda x: x.split(';')[1])
resultData['Rating'] =Data['User-ID,ISBN,Book-Rating'].apply(lambda x: x.split(';')[2] if len(x.split(';')) == 3  else 0)
resultData.to_csv('./CleanData/bookrating.csv')
#%%
#清理用户表
path = './data/BX-Users.csv'
Data = pd.read_csv(path, sep=None)
resultData = pd.DataFrame()
Data=Data.astype(str)
resultData['UserID'] =Data['User-ID;Location;Age'].apply(lambda x: x.split(';')[0] if len(x.split(';')) == 2 else 'NULL')
resultData['Username'] =Data['User-ID;Location;Age'].apply(lambda x: x.split(';')[1] if len(x.split(';')) == 2 else 'NULL')
resultData['Location'] =Data['Unnamed: 1']
resultData['Age'] =Data['Unnamed: 2'].apply(lambda x: x.split(';')[1] if len(x.split(';')) == 2 else 'NULL')
resultData.to_csv('./CleanData/user.csv')

#%%
#清理数据表
path = './data/BX-Books.csv'
Data = pd.read_csv(path, sep=None)
#'ISBN;Book-Title;Book-Author;Year-Of-Publication;Publisher;Image-URL-S;Image-URL-M;Image-URL-L'
Data['text'] = Data['ISBN;Book-Title;Book-Author;Year-Of-Publication;Publisher;Image-URL-S;Image-URL-M;Image-URL-L']
resultData = pd.DataFrame()
Data=Data.astype(str)
resultData['BookID'] =Data['text'].apply(lambda x: x.split(';')[0] )
resultData['BookTitle'] =Data['text'].apply(lambda x: x.split(';')[1] )
resultData['BookAuthor'] =Data['text'].apply(lambda x: x.split(';')[2] if len(x.split(';')) >= 3 else 'NULL' )
resultData['PubilcationYear'] =Data['text'].apply(lambda x: x.split(';')[3] if len(x.split(';')) >= 4 else 'NULL' )
resultData['PubilcationYear'] = resultData['PubilcationYear'].apply(lambda x: x if type(x) == int else '2010')

resultData['Publisher'] =Data['text'].apply(lambda x: x.split(';')[4] if len(x.split(';')) >= 5 else 'NULL' )

resultData['ImageS'] =Data['text'].apply(lambda x: x.split(';')[5] if len(x.split(';')) >= 6 else 'NULL' )
resultData['ImageM'] =Data['text'].apply(lambda x: x.split(';')[6] if len(x.split(';')) >= 7 else 'NULL' )
resultData['ImageL'] =Data['text'].apply(lambda x: x.split(';')[7] if len(x.split(';')) >= 8 else 'NULL' )
resultData.to_csv('./CleanData/book.csv')
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 00:01:50 2018

@author: Administrator
"""

from flask import Flask, render_template, request 
from flask import jsonify
import pandas as pd
import pymysql
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = "dfdfdffdad"


class BookSqlTools:
    #链接MYSQL数据库
    #读取出来转化成pandas的dataframe格式

    def LinkMysql(self, sql):
        try:
            connection = pymysql.connect(user="root",
                                         password="470581985",
                                         port=3306,
                                         host="127.0.0.1",   #本地数据库  等同于localhost
                                         db="Book",
                                         charset="utf8")
            cur = connection.cursor()
            print("Mysql数据库连接成功")
        except Exception as e:
            print("Mysql数据库连接失败：%s" % e)
        try:
            cur.execute(sql)
            print("SQL语句正确")
        except Exception as e:
            print("SQL语句错误：{}".format(e))
        try:
            result1 = cur.fetchall()
            title1 = [i[0] for i in cur.description]
            Main = pd.DataFrame(result1)
            Main.columns = title1
            print("读取Mysql数据库数据成功")
        except Exception as e:
            print("读取Mysql数据库数据失败：{}".format(e))
        return Main
    

    #数据库中的表插入数据
    def UpdateMysqlTable(self, data, sql_qingli, sql_insert):
        try:
            connection = pymysql.connect(user="root",
                                         password="470581985",
                                         port=3306,
                                         host="127.0.0.1",   #本地数据库  等同于localhost
                                         db="Book",
                                         charset="utf8")
            cursor = connection.cursor()
            print("Mysql数据库连接成功")
        except Exception as e:
            print("Mysql数据库连接失败：%s" % e)
        try:
            cursor.execute(sql_qingli)
        except:
            print("未执行建表的SQL语句")
        try:
            for i in data.index:
                x = list(pd.Series(data.ix[i,].astype(str)))
                sql = sql_insert.format(tuple(x))
                print(sql)
                try:
                    cursor.execute(sql)
                except:
                    print("Mysql数据库数据插入失败")
            print("Mysql数据库数据插入成功")
        except Exception as e:
            connection.rollback()
            print("Mysql数据库数据插入失败%s" % e)
        connection.commit()
        cursor.close()
        connection.close()


BookInfoInsert = BookSqlTools()

#--------------------------------------------------------------------------
#读取本地的User.csv文件  在数据库中建一个User表   将User.csv内容插入到数据库中
#--------------------------------------------------------------------------

User = pd.read_csv('CleanData/user.csv')
del User['Unnamed: 0']

createUserSql = '''CREATE TABLE User         
               (UserID                 INT(10)   ,
               Username                VARCHAR(100)  ,
               Location                VARCHAR(100) ,
                 Age                    VARCHAR(100) );'''

UserSql_insert='insert into User (UserID,Username,Location,Age) values {}'

BookInfoInsert.UpdateMysqlTable(User,createUserSql,UserSql_insert)

#--------------------------------------------------------------------------
#读取本地的book.csv文件  在数据库中建一个Books表   将book.csv内容插入到数据库中
#--------------------------------------------------------------------------

Book = pd.read_csv('CleanData/book.csv')
del Book['Unnamed: 0']

createBooksSql =''' CREATE TABLE Books         
               (BookID                    INT(10)   ,
                BookTitle                VARCHAR(100)  ,
                BookAuthor               VARCHAR(100) ,
                PubilcationYear          VARCHAR(100) );'''

BooksSql_insert='insert into Books (BookID,BookTitle,BookAuthor,PubilcationYear) values {}'


BookInfoInsert.UpdateMysqlTable(Book,createBooksSql,BooksSql_insert)

#--------------------------------------------------------------------------
#读取本地的bookrating.csv文件  在数据库中建一个Bookrating表   将bookrating.csv内容插入到数据库中
#--------------------------------------------------------------------------

Rating = pd.read_csv('CleanData/bookrating.csv')
del Rating['Unnamed: 0']

createBookratingSql = '''CREATE TABLE Bookrating        
               (UserID                    INT(10)   ,
                BookID                VARCHAR(100)  ,
                Rating                VARCHAR(100)  );'''          

BookratingSql_insert='insert into Bookrating (UserID,BookID,Rating) values {}'

BookInfoInsert.UpdateMysqlTable(Rating,createBookratingSql,BookratingSql_insert)

#--------------------------------------------------------------------------
#读取本地的Booktuijian.csv文件  在数据库中建一个Booktuijian表   将Booktuijian.csv内容插入到数据库中
#--------------------------------------------------------------------------

Booktuijian = pd.read_csv('CleanData/booktuijian.csv')
Booktuijian['score'] = Booktuijian['score'].apply(lambda x: round(x,2))
Booktuijian['score'] = 10*(Booktuijian['score'])/(max(Booktuijian['score']))


del Booktuijian['Unnamed: 0']

createBookrecomql = '''CREATE TABLE Booktuijian        
               (BookID                    INT(100)  ,
                UserID                    INT(10)   ,
                score                   FLOAT(5,3)   );'''  

BooktuijianSql_insert='insert into Booktuijian (BookID,UserID,score) values {}'

BookInfoInsert.UpdateMysqlTable(Booktuijian,createBookrecomql ,BooktuijianSql_insert)

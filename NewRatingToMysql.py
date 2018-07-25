

import pandas as pd
import pymysql

#--------------------------------------------------------------------------
#读取老师新给的的rating.csv文件    将rating.csv内容插入到Bookrating数据表中
#--------------------------------------------------------------------------
Rating = pd.read_csv('CF/rating.csv')
del Rating['Unnamed: 0']
       

BookratingSql_insert='insert into Bookrating (UserID,BookID,Rating) values {}'

connection = pymysql.connect(user="root",
                                         password="123456",
                                         port=3306,
                                         host="127.0.0.1",   #本地数据库  等同于localhost
                                         db="Book",
                                         charset="utf8")
cursor = connection.cursor()
try:
    for i in Rating.index:
        x = list(pd.Series(Rating.ix[i,].astype(str)))
        sql = BookratingSql_insert.format(tuple(x))
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

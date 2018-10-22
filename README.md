
------------------------------------------------------------------------------------------------
# 智能图书推荐系统                          
------------------------------------------------------------------------------------------------

[互联网访问地址](http://198.56.183.11:8080) 

[数据集下载地址](http://www2.informatik.uni-freiburg.de/~cziegler/BX/) 

 `主页`<br>
<img src="./image/img1.png" width="350" height="250"><br>
`搜索功能`<br>
<img src="./image/img2.png" width="350" height="250"><br>
`登录`<br>
<img src="./image/img3.png" width="350" height="250"><br>
`推荐`<br>
<img src="./image/img4.png" width="350" height="250"><br>

## V1.0.0.2 更新

    1.优化了搜索框的样式
    2.优化了整体配色
    3.优化了书籍排版，对名字长的书籍会自动省去保留开头。
    4.新增了一个书籍详情页面（基于书本的推荐可以在里面做）
    5.丰富了搜索内容 

## V1.0.0.1 更新

    1.增加了一个搜索引擎功能，可以输入书名做对应的查询，此功能还有待完善
    2.增加了对推荐书籍的评分功能。
    3.增加了查看历史评分书籍的功能。


## 所需运行环境

    使用python3.6作为编程语言。使用mysql作为数据库存储.
    需要安装pandas,flask，pymysql.
    安装方式:
    cmd下
    pip install pandas
    pip install flask
    pip install pymysql

 
## 联系作者：QQ：470581985

## 项目源码介绍
>     图书推荐系统
>        data               >这个文件夹中存放数据集，数据集比较杂乱。
>>         
>>       BX-Books.csv     >关于27万条的数据信息，涉及书籍编号，书籍名，书籍作者....
>>       BX-Users.csv     >关于27万条的用户信息，涉及用户ID，用户区县，用户省份，用户年龄。
>>       Rating1M.csv
>         CleanData         >这个文件夹中存放清洗好的数据集，将上面数据清理出需要的数据。
>>
>>       book.csv         >关于27万条的数据信息，保留书籍编号，书籍名，书籍作者，出版年份。
>>       user.csv         >关于27万条的用户信息，保留了用户ID，用户区县，用户省份，用户年龄。
>>                   并且将用户ID,和用户区县作为账号密码用于网站登录。
>>       bookrating.csv   >关于100万条的用户对数据的评分数据。保留用户ID，书籍ID，评分。（评分1-10为标准）
>>       booktuijian.csv  >关于10个测试用户和对其推荐书籍的信息。涉及用户ID，书籍ID，推荐指数。（评分1-10为标准）
>        BookWebAPI.py     >启动这个文件开启服务器。启动方式：在更目录下进入cmd输入    python BookWebAPI.py  
>        CleanCSV.py       >清洗原先杂乱的csv文件，保存到cleanData文件夹下面。
>        CSVToMysql.py     >将清洗好的文件，即CleanData里面的文件，导入到mysql中。
>        CF                >协同过滤1：CF 算法
>        slope one         >协同过滤2：slope one 算法
>        其他文件夹          >提供给前端页面和前端页面的依赖


##项目启动方式：

[数据集下载地址](http://www2.informatik.uni-freiburg.de/~cziegler/BX/)

    注意下载好的数据集导入到mysql中，代码可能不能直接跑出来，可以结合代码思路自行修改。
    1.首先在mysql建立一个数据库，库名为Book。
    2.运行CSVToMysql.py文件 将数据导入到mysql中。
    3.运行NewRatingToMysql.py文件 将数据导入到mysql中。
    4.进入BookwebAPI 运行即可。  登录的账号为user表中的userID，密码为user表中的Username
    如果需要测试推荐功能，可以登录usertuijian表中的userid对应的账户。（账号为userid，密码为usename，存在user表中）可以对推荐的书籍从新打分。    


##项目思路：

    本项目实现了3个图书推荐功能：
    1 基于书籍的推荐，将书籍按评论平均值排序，将前10个推送给用户。
    2 基于CF（协同过滤）算法的推荐，从登录用户阅读的书籍，寻找具有相同兴趣的用户，并将这些用户阅读的书籍计算求得匹配度。
     按匹配度将前十个推送给用户。
    3 基于slope one 的推荐。slope one讲解：

        用户\商品   商品1 商品2
        用户  1      3     4
        用户  2      4     ？

       从上表中预测用户2对商品2的评分时采用SlopeOne算法计算方式为：R(用户2，商品2) = 4 +（4-3）= 5
      这就是 SlopeOne 推荐的基本原理，它将用户的评分之间的关系看作简单的线性关系：Y = X + b


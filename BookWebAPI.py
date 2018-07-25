from flask import *
import pandas as pd
import pymysql
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "dfdfdffdad"


def LinkMysql(sql):
    try:
        connection = pymysql.connect(user="root",
                                     password="123456",
                                     port=3306,
                                     host="127.0.0.1",   #本地数据库  等同于localhost
                                     db="Book",
                                     charset="utf8")
        cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    except Exception as e:
        print("Mysql数据库连接失败：%s" % e)
    try:
        cur.execute(sql)
    except Exception as e:
        print("SQL语句错误：{}".format(e))
    try:
        result1 = cur.fetchall()
        Main = pd.DataFrame(result1)
    except Exception as e:
        print("读取Mysql数据库数据失败：{}".format(e))
    return Main

def getLoginDetails():
    '''
    如果登录后，会保留登录信息。session记录
    '''
    conn = pymysql.connect(user="root",
                                 password="123456",
                                 port=3306,
                                 host="127.0.0.1",   #本地数据库  等同于localhost
                                 db="Book",
                                 charset="utf8")
    cur = conn.cursor()
    if 'userid' not in session:
        loggedIn = False
        firstName = ''
        noOfItems = [0]
        oldbook = [0]
    else:
        loggedIn = True
        cur.execute("SELECT UserID, Username FROM User WHERE UserID = " + session['userid'] )
        firstName,userId = cur.fetchone()
        try:
            sql = "SELECT count(1) FROM booktuijian WHERE UserID = " + str(firstName)
            sql2 = "SELECT count(1) FROM bookrating WHERE UserID = " + str(firstName)
            cur.execute(sql)
            noOfItems = cur.fetchone()
            cur.execute(sql2)
            oldbook = cur.fetchone()
        except:
            noOfItems = [0]
            oldbook = [0]
    conn.close()
    return (loggedIn, firstName, str(noOfItems[0]),str(oldbook[0]))


@app.route("/")
def root():
    '''
    主页面
    '''
    loggedIn, firstName, noOfItems,oldbook = getLoginDetails()
    itemDatasql = 'SELECT BookTitle, BookAuthor,BookTitle,BookID,ImageM FROM Books LIMIT 10'
    itemData = LinkMysql(itemDatasql)
    try:

        likeDatasql = '''select 
                                a.BookTitle,
                                a.BookAuthor,
                                a.PubilcationYear,
                                a.BookID,
                                score,
                                a.ImageM 
                                from (SELECT * from books ) a  
                                LEFT  JOIN booktuijian as b on a.BookID = b.BookID where b.UserID = {}
        '''.format(session['userid'])
        likeData = LinkMysql(likeDatasql)
        likeData = likeData.sort_values(by='score',ascending=False)
    except:    
        likeDatasql = 'SELECT BookTitle, BookAuthor,BookTitle,BookID FROM Books where BookID = 0393045218 or BookID = 0345417623 '
        likeData = LinkMysql(likeDatasql) 
        likeData.dropna()
        likeData['score'] = 0
   
    categoryData=[['2010','教育读物']]
    
    itemDatares=[]
    likeDatares=[]
    for i in itemData.index:
        x = tuple(pd.Series(itemData.ix[i,].astype(str))) 
        itemDatares.append(x)
    for i in likeData.index:
        x = tuple(pd.Series(likeData.ix[i,].astype(str))) 
        likeDatares.append(x)   

    return render_template('home.html', itemData=[itemDatares], oldbook=oldbook,loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData, likeData=[likeDatares])


@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    '''
    注册
    '''
    if request.method == 'POST':
        UserID = request.form['userid']
        Username = request.form['username']
        Age = request.form['age']
    
        conn = pymysql.connect(user="root",
                                 password="123456",
                                 port=3306,
                                 host="127.0.0.1",   #本地数据库  等同于localhost
                                 db="Book",
                                 charset="utf8")
        cur = conn.cursor()
        try:
            cur.execute("insert into User (UserID,Username,Location,Age) values ('{}','{}','{}')".format(UserID, Username, Age))
            con.commit()
            print("Saved Successfully")
        except:
            con.rollback()
            print("Error occured")
        conn.close()
        return redirect(url_for('editProfile'))


@app.route("/loginForm")
def loginForm():
    '''
    登录
    '''
    if 'userid' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')


def is_valid(userid, username):
    '''
    登录验证
    '''
    conn = pymysql.connect(user="root",
                         password="123456",
                         port=3306,
                         host="127.0.0.1",  #本地数据库  等同于localhost
                         db="Book",
                         charset="utf8")
    cur = conn.cursor()
    try:
        sql = "SELECT UserID, Username FROM User where UserID={} and Username ='{}'".format(userid, username)
        cur.execute(sql)
        data = cur.fetchone()
        conn.close()
        return True
    except:
        conn.close()
        return False

@app.route("/login", methods = ['POST', 'GET'])
def login():
    '''
    登录
    '''
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        if is_valid(userid, username):
            session['userid'] = userid
            return redirect(url_for('root'))
        else:
            error = '该用户ID还未注册，或姓名输入错误'
            return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    '''
    退出登录，注销
    '''
    session.pop('userid', None)
    return redirect(url_for('root'))


@app.route("/registerationForm")
def registrationForm():
    '''
    注册
    '''
    return render_template("register.html")

@app.route("/search",methods = ['POST', 'GET'])
def search():
    '''
    search
    '''
    if request.method == 'GET':
        checked = ['checked="true"', '', '']
        wd =  request.values.get('wd')
        sql = "SELECT * from Books where BookTitle like '%{}%' ".format(wd)
        Data = LinkMysql(sql)
       
        BookTitle = Data['BookTitle'].values
        BookAuthor = Data['BookAuthor'].values
        
        Pagesize=10
        page = []
        for i in range(1, (len(Data) // 10 + 2)):
            page.append(i)
        Data = Data.head(10)
        docs =[]
        for i in range(len(Data)):
            doc  = {'url': '', 'title': BookTitle[i], 'snippet': BookAuthor[i], 'datetime': '2018-01-02', 'time': 'Author:', 'body': BookAuthor[i],
                   'id': wd, 'extra': []}
            docs.append(doc)

        return render_template('high_search.html', checked=checked, key=wd, docs=docs, page=page,
                                   error=True)



@app.route("/cart",methods = ['POST', 'GET'])
def cart():
    if 'userid' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems,oldbook = getLoginDetails()
    conn = pymysql.connect(user="root",
                                 password="123456",
                                 port=3306,
                                 host="127.0.0.1",   #本地数据库  等同于localhost
                                 db="Book",
                                 charset="utf8")
    cur = conn.cursor()

    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        UserID = session['userid']
        BookID = data['id']
        score = data['score']

        sql='''UPDATE Booktuijian
                        SET
                        score={}
                        WHERE UserID="{}" and BookID="{}" '''.format(int(score),UserID,BookID)

        cur.execute(sql)
        conn.commit()
        sql2 = '''SELECT COUNT(1) FROM Bookrating WHERE UserID="{0}" and BookID="{1}" '''.format(UserID,BookID)
        cur.execute(sql2)
        res = cur.fetchone()  
        
        if res[0]:
            sql3=   '''UPDATE Bookrating SET Rating='{2}' WHERE UserID="{0}" and BookID="{1}"  '''.format(UserID,BookID,int(score))
        else:
            sql3= ''' insert into Bookrating (UserID,BookID,Rating) values ('{0}','{1}','{2}') '''.format(UserID,BookID,int(score))

        cur.execute(sql3)
        conn.commit()
        print('插入数据成功')
    itemDatasql  = '''select 
                                BookTitle,
                                BookAuthor,
                                PubilcationYear,
                                a.BookID,
                                score,
                                a.ImageM 
                                from (SELECT * from books ) a  
                                LEFT  JOIN booktuijian as b on a.BookID = b.BookID where b.UserID = '{}'
                                '''.format(session['userid'])
    itemData = LinkMysql(itemDatasql)
    products=[]
    for i in itemData.index:
        x = tuple(pd.Series(itemData.ix[i,].astype(str))) 
        products.append(x)
    return render_template("cart.html", products = products,oldbook=oldbook,  loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/oldcart",methods = ['POST', 'GET'])
def oldcart():
    if 'userid' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems,oldbook = getLoginDetails()
    conn = pymysql.connect(user="root",
                                 password="123456",
                                 port=3306,
                                 host="127.0.0.1",   #本地数据库  等同于localhost
                                 db="Book",
                                 charset="utf8")
    cur = conn.cursor()

    itemDatasql  = '''select 
                                BookTitle,
                                BookAuthor,
                                PubilcationYear,
                                a.BookID,
                                Rating,
                                ImageM 
                                from (SELECT * from bookrating ) a  
                                LEFT  JOIN  books as b on a.BookID = b.BookID where a.UserID = '{}'
                                '''.format(session['userid'])
    itemData = LinkMysql(itemDatasql)
    products=[]
    for i in itemData.index:
        x = tuple(pd.Series(itemData.ix[i,].astype(str))) 
        products.append(x)
    return render_template("cart.html", products = products,oldbook=oldbook, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)




if __name__ == '__main__':
    app.run(debug=True)
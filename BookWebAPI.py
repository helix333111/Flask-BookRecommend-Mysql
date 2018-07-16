from flask import *
import pandas as pd
import pymysql


app = Flask(__name__)
app.config['SECRET_KEY'] = "dfdfdffdad"


def LinkMysql(sql):
    try:
        connection = pymysql.connect(user="root",
                                     password="470581985",
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
                                 password="470581985",
                                 port=3306,
                                 host="127.0.0.1",   #本地数据库  等同于localhost
                                 db="Book",
                                 charset="utf8")
    cur = conn.cursor()
    if 'userid' not in session:
        loggedIn = False
        firstName = ''
        noOfItems = [0]
    else:
        loggedIn = True
        cur.execute("SELECT UserID, Username FROM User WHERE UserID = '" + session['userid'] + "'")
        firstName,userId = cur.fetchone()
        try:
            sql = "SELECT count(1) FROM Bookrating WHERE UserID = " + str(firstName)
            cur.execute(sql)
            noOfItems = cur.fetchone()
        except:
            noOfItems = [0]
    conn.close()
    return (loggedIn, firstName, str(noOfItems[0]))


@app.route("/")
def root():
    '''
    主页面
    '''
    loggedIn, firstName, noOfItems = getLoginDetails()
    itemDatasql = 'SELECT BookTitle, BookAuthor,BookTitle,BookID FROM Books LIMIT 10'
    itemData = LinkMysql(itemDatasql)
    itemData['Image'] = 'x.jpg'
    try:
        tuijiansql = 'SELECT BookID,score FROM Booktuijian where UserID ={}'.format(session['userid'])
        tuijiandf = LinkMysql(tuijiansql) 
   
        sqllist = []
        for i in tuijiandf['BookID']:
            sqllist.append("BookID = {} ".format(i))
        likeDatasql = 'SELECT BookTitle, BookAuthor,BookTitle,BookID FROM Books where '+' or '.join(sqllist)
        likeData = LinkMysql(likeDatasql) 
       
        likeData = pd.merge(likeData,tuijiandf,left_on='BookID', right_on='BookID')
        likeData.dropna()
        likeData = likeData.sort_values(by='score',ascending=False)
    except:    
        likeDatasql = 'SELECT BookTitle, BookAuthor,BookTitle,BookID FROM Books where BookID = 0393045218 or BookID = 0345417623 '
        likeData = LinkMysql(likeDatasql) 
    likeData['Image'] = 'x.jpg' 
    categoryData=[['2010','小学生']]
    
    itemDatares=[]
    likeDatares=[]
    for i in itemData.index:
        x = tuple(pd.Series(itemData.ix[i,].astype(str))) 
        itemDatares.append(x)
    for i in likeData.index:
        x = tuple(pd.Series(likeData.ix[i,].astype(str))) 
        likeDatares.append(x)   

    return render_template('home.html', itemData=[itemDatares], loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData, likeData=[likeDatares])


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
                                 password="470581985",
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
                         password="470581985",
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



if __name__ == '__main__':
    app.run(debug=True)
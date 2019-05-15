from utils import load_config
from utils import mysql
UserID = 'adam'
BookID = '12'
config = load_config()
mysql = mysql(config['mysql'])
sql = '''SELECT sum(score) as score FROM Booktuijian WHERE UserID="{0}" and BookID="{1}" '''.format(UserID,BookID)
a = mysql.fetchone_db(sql)
print(a)
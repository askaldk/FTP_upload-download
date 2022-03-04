from importlib.metadata import files
import pymysql


conn = pymysql.connect(  # 需從 My.ini 設定 MySQL server variable datadir，修改後才有權限操作存檔資料夾到指定位置
    host='127.0.0.1',
    user='root',
    password='12345',
    database='ul_fdcc'
)

cursor = conn.cursor()
sql = '''                                           
   SELECT * from LogRecord
    '''

cursor.execute(sql)
datas=cursor.fetchall()
for data in datas:
    print(data)

cursor.close()

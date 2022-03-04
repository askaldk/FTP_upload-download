from cmath import e
from ftplib import FTP
from pymysql.constants import CLIENT
import time
import pymysql


class ftpConnection:
    ftpHost = '127.0.0.1'
    ftpPort = '21'
    ftpUser = 'Jack'
    ftpPwd = '12345'


conn = pymysql.connect(  # 需從 My.ini 設定 MySQL server variable datadir，修改後才有權限操作存檔資料夾到指定位置                         # (但是windows好像不行改資料夾，不然 sql server會直接開不了)
    host='127.0.0.1',
    user='root',
    password='12345',
    database='yilin_backup',
    client_flag=CLIENT.MULTI_STATEMENTS
)


dataBase_localPath = r"C:\ProgramData\MySQL\MySQL Server 8.0\Data\yilin_backup"
ftpPath = "/cc/database"
count = 0
tableName = "yilin_backup.logrecord"

def ftpToDatabase():
    sql = '''
    delete from '''+tableName+''';
    load data infile \''''+ftpFile+'''\' into table '''+tableName+''' fields terminated by ',' lines terminated by '\\n';
    
    '''
    print(sql)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        print('插入資料成功 !')
        datas = cursor.fetchall()
        for data in datas:
            print(data)
        conn.commit()
        cursor.close()
    except e:
        print('database 插入資料失敗 !')

print("begin: "+time.ctime())
time.sleep(1)

ftp = FTP(ftpConnection.ftpHost, ftpConnection.ftpUser, ftpConnection.ftpPwd)
ftp.cwd(ftpPath)
while(True):
    ftpFileList = ftp.nlst()
    for ftpFile in ftpFileList:
        try:
            with open(dataBase_localPath+'/'+ftpFile, "wb") as file:     # 本地端要儲存檔案的地方
                ftp.retrbinary('RETR '+ftpFile, file.write)     # 下載檔案
                print('資料下載到資料庫 data directory 成功\n')
                file.close()
        except:
            print('FTP 傳送到 database_loaclalPath 失敗\n')
        print(ftpFile)
        ftpToDatabase()
        
ftp.quit      # 結束連線

# \''''+ftpFile+'''\'  '''+tableName+'''

# load data infile \''''+ftpFile+'''\' into table '''+tableName+''' fields terminated by ',' lines terminated by '\\n';
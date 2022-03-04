from cmath import e
from ftplib import FTP
import pymysql
import time
import os


class ftpConnection:
    ftpHost = '127.0.0.1'
    ftpPort = '21'
    ftpUser = 'Jack'
    ftpPwd = '12345'


dataBase_localPath = r'C:\ProgramData\MySQL\MySQL Server 8.0\Data\ul_fdcc'
ftpPath = "/cc/database"

count = 0

conn = pymysql.connect(
    host='192.168.68.135',
    user='tctcore',
    password='tctcore',
    database='ul_fdcc'
)

while(True):

    print("\nbegin: "+time.ctime()+"")
    time.sleep(1)
    print("end: "+time.ctime()+"\n")
    try:                         # FTP 建立連線
        ftp = FTP(ftpConnection.ftpHost,
                  ftpConnection.ftpUser, ftpConnection.ftpPwd)
        print('FTP 連線成功\n')
    except ConnectionError:
        print('FTP 連線失敗\n')

    # 將 mysql 轉成檔案(.txt)
    fileName = '{}.txt'.format(count)
    if os.path.isfile(dataBase_localPath+'/'+fileName):  # 判斷檔案是否已經存在，如果已經存在就刪除!
        print('檔案'+fileName+'已存在，刪除!\n')
        dataFile = os.path.join(dataBase_localPath, fileName)
        os.remove(dataFile)
    else:
        print('檔案不存在\n')

    try:
        cursor = conn.cursor()
    except:
        print('db connect 建立成功，但 cursor 獲取失敗.')

    sql = '''                                           
    select * from LogRecord
        into outfile  \''''+fileName+'''\'   
        fields terminated by ','

    '''
# \''''+fileName+'''\'
    try:
        cursor.execute(sql)
        print('success transfer to '+fileName+' file')
    except e:
        print('database 轉 .txt 檔案失敗!')

    if(count < 20):
        count += 1
    else:
        count = 0

    time.sleep(1)

    cursor.close()

    localFileList = os.listdir(dataBase_localPath)
    for localFile in localFileList:  # 開啟本機端資料夾下所有檔案
        if('.txt' in localFile):
            print(localFile)
            with open(dataBase_localPath+"/"+localFile, "rb")as file:
                ftp.storbinary('STOR '+ftpPath+"/"+localFile, file)  # FTP 上傳檔案
                file.close()
    ftp.quit      # 結束連線

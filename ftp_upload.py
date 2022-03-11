from cmath import e
from ftplib import FTP
import pymysql
import time
import os


dataBase_name = 'yoyo'
dataBase_localPath = '/var/lib/mysql/'+dataBase_name
ftpPath = '/home/site/database'


class ftpConnection:
    ftpHost = '192.168.223.131'
    ftpPort = '21'
    ftpUser = 'tctcore'
    ftpPwd = 'Tctcore@1'


def new_file():       # 抓取最新檔案，依照檔案最後修改時間進行抓取
    newFileList=[]
    fileList = os.listdir(dataBase_localPath)
    for file in fileList:
        if file.endswith('.txt'):
            newFileList.append(file)
    if not newFileList:
        count = 0
        return count
    else:
        newFileList.sort(key=lambda fn: os.path.getmtime(dataBase_localPath+'/'+fn))
        newestFileFormat = os.path.splitext(newFileList[-1])[0]
        count = int(newestFileFormat)
        return count


count = new_file() + 1

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='12345',
    database='yoyo'
)

while(True):

    print("\nbegin: "+time.ctime()+"")
    time.sleep(10)
    try:                         # FTP 建立連線
        ftp = FTP(ftpConnection.ftpHost,
                  ftpConnection.ftpUser, ftpConnection.ftpPwd)
        print('FTP 連線成功\n')
    except ConnectionError:
        print('FTP 連線失敗\n')

    fileName = '{}.txt'.format(count)

    if os.path.exists(dataBase_localPath+'/'+fileName):  # 判斷檔案是否已經存在，如果已經存在就刪除!
        print('檔案'+fileName+'已存在，刪除!\n')
        dataFile = os.path.join(dataBase_localPath, fileName)
        os.remove(dataFile)
    else:
        print('檔案不存在\n')

    try:
        cursor = conn.cursor()
    except:
        print('db connect 建立成功，但 cursor 獲取失敗.')

    # 將 mysql 轉成檔案(.txt)
    sql = '''                                           
    select * from logrecord
        into outfile  \''''+fileName+'''\'   
        fields terminated by ','
    '''

    try:
        cursor.execute(sql)
        print('success transfer to '+fileName+' file')
    except e:
        print('database 轉 .txt 檔案失敗!')

    cursor.close()

    try:
        with open(dataBase_localPath+"/"+fileName, "rb")as file:
            ftp.storbinary('STOR '+ftpPath+"/"+fileName, file)  # FTP 上傳檔案
            file.close()
    except e:
        print('FTP 檔案上傳失敗!')

    if(count < 99):
        count += 1
    else:
        count = 0

    ftp.quit      # 結束連線

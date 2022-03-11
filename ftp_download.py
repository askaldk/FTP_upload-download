from cmath import e
from pymysql.constants import CLIENT
from time import sleep
import time
import pymysql
import os


conn = pymysql.connect(  # 需從 My.ini 設定 MySQL server variable datadir，修改後才有權限操作存檔資料夾到指定位置                         # (但是windows好像不行改資料夾，不然 sql server會直接開不了)
    host='127.0.0.1',
    user='root',
    password='Tctcore@2',
    database='yoyo',
    client_flag=CLIENT.MULTI_STATEMENTS
)

dataBaseName = 'yoyo'
dataBase_localPath = '/var/lib/mysql/'+dataBaseName
ftpPath = '/home/site/database'
tableName = "yoyo.logrecord"


def find_txt_file():
    newFileList = []
    fileList = os.listdir(dataBase_localPath)
    for file in fileList:
        if file.endswith('.txt'):
            newFileList.append(file)
    return newFileList


def new_file():       # 抓取最新檔案
    newFileList = find_txt_file()
    if not newFileList:
        sleep(1)
        return new_file()
    else:
        newFileList.sort(key=lambda fn: os.path.getmtime(
            dataBase_localPath+'/'+fn))
        newFileFormat = os.path.splitext(newFileList[-1])[0]
        count = int(newFileFormat)
        return count


def remove_file(count):
    file = '{}.txt'.format(count)
    newfileList = find_txt_file()
    for newfile in newfileList:
        if (newfile == file):
            print('這是最新的檔案:'+file+'')
        else:
            os.remove(dataBase_localPath+'/'+newfile)


while(True):
    count = new_file()
    remove_file(count)
    ftpFile = '{}.txt'.format(count)

    sql = '''
    delete from '''+tableName+''';
    load data infile \''''+ftpPath+'/'+ftpFile+'''\' into table '''+tableName+''' fields terminated by ',' lines terminated by '\\n';

    '''
    print(sql)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        print(''+ftpFile+':資料更新成功 !')
        datas = cursor.fetchall()
        for data in datas:
            print(data)
        conn.commit()
        cursor.close()
    except e:
        print('database 插入資料失敗 !')

    print("end_time: "+time.ctime())

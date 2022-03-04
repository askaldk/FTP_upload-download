import pymysql
import time
import os
# conn = pymysql.connect(
#     host='192.168.68.135',
#     user='tctcore',
#     password='tctcore',
#     database='ul_fdcc'
# )

conn = pymysql.connect(  # 需從 My.ini 設定 MySQL server variable datadir，修改後才有權限操作存檔資料夾到指定位置
    host='127.0.0.1',
    user='root',
    password='12345',
    database='ul_fdcc'
)

count = 0

dataBase = r'C:\ProgramData\MySQL\MySQL Server 8.0\Data\ul_fdcc'
while(True):

    fileName = '{}.txt'.format(count)
    if os.path.isfile(dataBase+'/'+fileName):  # 判斷檔案是否已經存在，如果已經存在就刪除!
        print('檔案'+fileName+'已存在，刪除!')
        dataFile = os.path.join(dataBase, fileName)
        os.remove(dataFile)
    else:
        print('檔案不存在')
    cursor = conn.cursor()  # 將 mysql 轉成檔案(.txt)
    sql = '''                                           
    select * from LogRecord
        into outfile \''''+fileName+'''\'    
        fields terminated by ',' 
        lines terminated by '\n'       
    '''
    print('success transfer to '+fileName+' file')
    cursor.execute(sql)
    if(count < 20):
        count += 1
    else:
        count = 0

    time.sleep(1)

    cursor.close()

    # cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_NAME')
    # cursor.execute('SELECT COLUMN_NAME,ORDINAL_POSITION,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "user"')
    # cursor.execute('SELECT * from Information_Schema.TABLES')

    # cursor.execute('SELECT * FROM INFORMATION_SCHEMA.Columns Where Table_Name="RealAi_Memory"')

    # cursor.execute('SELECT UniKey FROM RealAi_Memory')
    # cursor.execute('SELECT * FROM LogRecord')
    # sqlData = cursor.execute('select * from ul_fdcc.LogRecord outfile C:/Users/black/OneDrive/桌面/noah/sqlToFile/0.txt')

from stat import FILE_ATTRIBUTE_SPARSE_FILE
import pymysql
import os

conn = pymysql.connect(  # 需從 My.ini 設定 MySQL server variable datadir，修改後才有權限操作存檔資料夾到指定位置                         # (但是windows好像不行改資料夾，不然 sql server會直接開不了)
    host='127.0.0.1',
    user='root',
    password='12345',
    database='yilin_backup'
)

ftpPath = "/cc/database"
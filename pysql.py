import pymysql

conn = pymysql.connect(
    host='192.168.68.135',
    user='tctcore',
    password='tctcore',
    database='ul_fdcc'
)
count = 0
localSqlToFilePath = 'C:/Users/black/OneDrive/桌面/noah/sqlToFile'


# cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY TABLE_NAME')
# cursor.execute('SELECT COLUMN_NAME,ORDINAL_POSITION,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "user"')
# cursor.execute('SELECT * from Information_Schema.TABLES')
# cursor.execute('SELECT "DataValue" FROM RealAi_Memory')
# cursor.execute('SELECT * FROM INFORMATION_SCHEMA.Columns Where Table_Name="RealAi_Memory"')
# cursor.execute('SELECT * FROM LogRecord')
while(True):
    fileName = '{}.txt'.format(count)
    cursor = conn.cursor()
    sql = '''
    select * into outfile  RealAi_Memory 
    '''
    sqlData = cursor.execute('select * into outfile '+localSqlToFilePath+'/'+fileName+' from ul_fdcc.RealAi_Memory ')
    print(sqlData)
    for row in cursor:
        print(row)
    count += 1
    print("success")
    cursor.close()
    conn.close()

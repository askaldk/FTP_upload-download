from ftplib import FTP, FTP_PORT
import time
import os


class ftpConnection:
    ftpHost = '127.0.0.1'
    ftpPort = '21'
    ftpUser = 'Jack'
    ftpPwd = '12345'


localPath = "C:/Users/black/OneDrive/桌面/noah/ftp_download"
remotePath = "/cc"




print("begin: "+time.ctime())
time.sleep(1)
print("end: "+time.ctime())
ftp = FTP(ftpConnection.ftpHost,
            ftpConnection.ftpUser, ftpConnection.ftpPwd)
localFileList = os.listdir(localPath)
for localFile in localFileList:     #開啟本機端資料夾下所有檔案
    with open(localPath+"/"+localFile, "rb")as file:
        ftp.storbinary('STOR '+remotePath+"/"+localFile,file)  #FTP 上傳檔案
        file.close()
ftp.quit      # 結束連線

from ftplib import FTP, FTP_PORT
import time
class ftpConnection:
    ftpHost = '127.0.0.1'
    ftpPort = '21'
    ftpUser = 'Jack'
    ftpPwd = '12345'

localPath="C:/Users/black/OneDrive/桌面/noah/ftp_download"
remotePath = "/cc/ppt pictures"
print("begin: "+time.ctime())
time.sleep(1)
print("end: "+time.ctime())
ftp = FTP(ftpConnection.ftpHost,ftpConnection.ftpUser,ftpConnection.ftpPwd)
ftp.cwd(remotePath)   # FTP server 端切換至指定的目錄
remoteListFile = ftp.nlst()   # 列出所有檔案或資料夾
print(remoteListFile)
for remoteFile in remoteListFile:
        with open(localPath+'/'+remoteFile ,"wb") as file:     # 本地端要儲存的檔案
            ftp.retrbinary('RETR '+remoteFile,file.write)     # 下載檔案
            file.close()
ftp.quit      # 結束連線
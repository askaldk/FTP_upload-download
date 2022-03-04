import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.68.135',username='tctcore',password='tctcore')

ftp = ssh.open_sftp()
filea = ftp.get('/home/tctcore/','#')
print(filea)

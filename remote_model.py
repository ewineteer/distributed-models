import paramiko
import glob
import os

sclient = paramiko.SSHClient()
sclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sclient.connect(hostname='192.168.0.202',username='paradigm',password='rocketship')
stdin,stdout,stderr=sclient.exec_command('cd C:/SUSTAIN')
stdin,stdout,stderr=sclient.exec_command('python3 C:/SUSTAIN/checkexec.py')
stdin,stdout,stderr=sclient.exec_command('dir')


sclient.close()




        filename = os.path.basename(file)
        topath = os.path.join(remotedir,filename)
        topaths.append(topath)

testinps = glob.glob('/home/eric/projects/CityofLA_Opti/Input/WQ/*.inp')

remotedir = 'C:/Projects/SCP_Test/ftp_test'

send_files(sclient,testinps[1:10],'C:/Projects/SCP_Test/ftp_test')
file = testinps[1]



sustainversion = '2.0'

class Clientfuncs:




def sustainexec(sclient,inppaths,flag=2):
    sclient.exec_command(f'START ')

import sys
import glob
import os
sys.path.append('/home/eric/projects/distributed-models')
import serverfuncs


filedir = '/home/eric/projects/distributed-models/Input/cola-wilmington4'

client1 = serverfuncs.connectclient(hostname='192.168.0.202')
clients = [client1]

batchname = 'cola-wilmington4'

def chunks(list, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield list[i::n]



def distribute_files(batchname, clients):
    filedir = os.path.join('/home/eric/projects/distributed-models/Input/', batchname)
    files = glob.glob(os.path.join(filedir, '*.inp'))
    filechunks = chunks(list=files, n=len(clients))
    for i,filechunk in enumerate(filechunks):
        print(i)
        filechunknames = [os.path.basename(filepath) for filepath in filechunk]
        remotepaths = [os.path.join('C:/SUSTAIN/Input/', batchname, filename) for filename in filechunknames]
        serverfuncs.sendfiles(clients[i], filechunk, remotepaths)

distribute_files('cola-wilmington4', clients)

serverfuncs.sendfiles(clients[0], ['/home/eric/projects/distributed-models/exec_client.py'], ['C:/SUSTAIN/exec_client.py'])

stdin,stdout,stderr = client1.exec_command('python3 C:/SUSTAIN/exec_client.py')

serverfuncs.getfolder(client1, '/home/eric/projects/distributed-models/Output/wilmington4/', 'C:/SUSTAIN/Output/TempOut/')

sess = serverfuncs.SSHSession(5)
sess
sess.get_all(remotepath= 'C:/SUSTAIN/Output/TempOut/', localpath = '/home/eric/projects/distributed-models/Output/TempOut/')
os.path.split('/home/eric/projects/distributed-models/Output/TempOut/')[0]

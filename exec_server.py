import sys
import glob
import os
sys.path.append('/home/eric/projects/distributed-models')
import serverfuncs


filedir = '/home/eric/projects/distributed-models/Input/cola-wilmington'

client1 = serverfuncs.connectclient(hostname='192.168.0.202')
clients = [client1]

batchname = 'cola-wilmington'

def chunks(list, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield list[i::n]


def distribute_files(batchname, clients):
    filedir = os.path.join('/home/eric/projects/distributed-models/Input/', batchname)
    files = glob.glob(os.path.join(filedir, '*.inp'))
    filechunks = chunks(list=files, n=2)
    for i,filechunk in enumerate(filechunks):
        print(i)
        filechunknames = [os.path.basename(filepath) for filepath in filechunk]
        remotepaths = [os.path.join('C:/SUSTAIN/Input/', batchname, filename) for filename in filechunknames]
        serverfuncs.sendfiles(clients[i], filechunk, remotepaths)


distribute_files('cola-wilmington', clients)


def sendfiles(sclient, localpaths, remotepaths):
    fclient = sclient.open_sftp()
    for i, path in enumerate(localpaths):
        remotedir = os.path.dirname(remotepaths[i])
        if direxists(fclient, remotedir):
            fclient.put(path, remotepaths[i])
        else:
            fclient.mkdir(remotedir)
            fclient.put(path, remotepaths[i])
    fclient.close()


serverfuncs.sendfiles(client1, ['/home/eric/projects/distributed-models/exec_client.py'], ['C:/SUSTAIN/exec_client.py'])

client1.exec_command('python3 C:/SUSTAIN/exec_client.py')

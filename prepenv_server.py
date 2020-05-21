import paramiko
import sys
import re

sys.path.append('/home/eric/projects/distributed-models')
import serverfuncs


sclient = serverfuncs.connectclient(hostname='192.168.0.202',
                                    username='paradigm', password='rocketship')


# Even if there is only one file to send, the paths MUST be in a list for this function to work.
remotefuncs.sendfiles(sclient, ['/home/eric/projects/distributed-models/prepenv_client.py'], ['C:/SUSTAIN/prepenv_client.py.py'])

sustaindirectory = 'c:/SUSTAIN'
sustainversion = 'SUSTAIN-2.0'
stdin, stdout, stderr = sclient.exec_command(f'python3 C:/SUSTAIN/prepenv_client.py {sustaindirectory} {sustainversion} {batchname}')

output = stdout.readlines()
errors = stderr.readlines()
sclient.close()

if errors:
    print(errors)

for line in output:
    if re.search('WARNING', line):
        print(line)

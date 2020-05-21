import paramiko
import re
import os
import pandas as pd


def direxists(sftp, path):
    try:
        sftp.stat(path)
        return True
    except FileNotFoundError:
        return False


# Even if there is only one file to send, the paths MUST be in a list for this function to work.
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


# Uhhhh I probably shouldn't store credentials in plaintext
def connectclient(hostname, username='paradigm', password='rocketship'):
    sclient = paramiko.SSHClient()
    sclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sclient.connect(hostname=hostname, username=username,
                    password=password)
    return(sclient)


def gen_inp(templatepath, inppath, modrep):
    with open(templatepath, 'r', encoding='utf_8') as template:
        with open(inppath, 'wt', encoding='utf_8', newline='\r\n') as output:
            text = template.read()
            text = re.sub(r'!(.*?)!', modrep, text)  # regex is black magic to me so good luck debugging this
            output.write(text)


class RepFuncs(object):
    lookup = {}

    def modrep(self, match):
        string = match.group()
        repstring = re.sub('!', '', string)
        if repstring in self.lookup.keys():
            replacement = self.lookup[repstring]
        else:
            replacement = repstring
        return(replacement)


# This function is pretty hacky, and makes a lot of assumptions about the Input
# .csv format. Consider improving.
def read_modparms(path):
    modparms = pd.read_csv(path)
    modparms = modparms[modparms['Key Value'].notnull()]
    keys = modparms['Key Value']
    keys = keys.astype(int)
    modparms = modparms.astype(str)
    modparms['Key Value'] = keys
    modparms = modparms.T
    modparms.columns = modparms.loc['Key Value', :]
    modparms = modparms.drop('Key Value')
    return(modparms)

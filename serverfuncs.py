import paramiko
import re
import os
import pandas as pd
import socket
from stat import S_ISDIR

'''
def remotedirexists(sftp, path):
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
        if remotedirexists(fclient, remotedir):
            fclient.put(path, remotepaths[i])
        else:
            fclient.mkdir(remotedir)
            fclient.put(path, remotepaths[i])
    fclient.close()

sclient = connectclient(hostname='192.168.0.202')
localdir = '/home/eric/projects/distributed-models/Output/wilmington4/'
remotedir = 'C:/SUSTAIN/Output/TempOut/'
fclient = sclient.open_sftp()
remoteiter = fclient.listdir_iter(path=remotedir)
for remotepath in remoteiter:
    remotepath_full = os.path.join(remotedir, remotepath)
    remote_subdirs = fclient.listdir(path=remotepath)

    getfiles()

# Unlike the sendfiles and getfiles functions, the paths SHOULD NOT be in a list.
def getfolder(sclient, localdir, remotedir):
    fclient = sclient.open_sftp()
    remotenames = fclient.listdir(remotedir)
    remotepaths = [os.path.join(remotedir, remotename) for remotename in remotenames]
    localpaths = [os.path.join(localdir, remotename) for remotename in remotenames]
    if not os.path.isdir(localdir):
        os.makedirs(localdir)
    for i, path in enumerate(remotepaths):
        fclient.get(path, localpaths[i])


def sftp_walk(fclient, remotepath):
    # Kindof a stripped down  version of os.walk, implemented for
    # sftp.  Tried running it flat without the yields, but it really
    # chokes on big directories.
    path=remotepath
    files=[]
    folders=[]
    for f in fclient.listdir_attr(remotepath):
        if S_ISDIR(f.st_mode):
            folders.append(f.filename)
        else:
            files.append(f.filename)
    print (path,folders,files)
    yield path,folders,files
    for folder in folders:
        new_path=os.path.join(remotepath,folder)
        for x in sftp_walk(new_path):
            yield x

def get_all(sclient, remotepath, localpath):
    fclient = sclient.open_sftp()
    #  recursively download a full directory
    #  Harder than it sounded at first, since paramiko won't walk
    self.fclient.chdir(os.path.split(remotepath)[0])
    parent=os.path.split(remotepath)[1]
    try:
        os.mkdir(localpath)
    except:
        pass
    for walker in sftp_walk(fclient, remotepath):
        try:
            os.mkdir(os.path.join(localpath,walker[0]))
        except:
            pass
        for file in walker[2]:
            get(os.path.join(walker[0],file),os.path.join(localpath,walker[0],file))


def getfiles(sclient, localpaths, remotepaths):
    fclient = sclient.open_sftp()
    for i, path in enumerate(remotepaths):
        localdir = os.path.dirname(localpaths[i])
        if os.path.exists(localdir):
            fclient.get(path, localpaths[i])
        else:
            fclient.mkdir(localdir)
            fclient.get(path, localpaths[i])
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

'''
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

class SSHSession(object):
    # Usage:
    # Detects DSA or RSA from key_file, either as a string filename or a
    # file object.  Password auth is possible, but I will judge you for
    # using it. So:
    # ssh=SSHSession('targetserver.com','root',key_file=open('mykey.pem','r'))
    # ssh=SSHSession('targetserver.com','root',key_file='/home/me/mykey.pem')
    # ssh=SSHSession('targetserver.com','root','mypassword')
    # ssh.put('filename','/remote/file/destination/path')
    # ssh.put_all('/path/to/local/source/dir','/path/to/remote/destination')
    # ssh.get_all('/path/to/remote/source/dir','/path/to/local/destination')
    # ssh.command('echo "Command to execute"')

    def __init__(self,hostname,username='root',key_file=None,password=None):
        #
        #  Accepts a file-like object (anything with a readlines() function)
        #  in either dss_key or rsa_key with a private key.  Since I don't
        #  ever intend to leave a server open to a password auth.
        #
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname,22))
        self.t = paramiko.Transport(self.sock)
        self.t.start_client()
        keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        key = self.t.get_remote_server_key()
        # supposed to check for key in keys, but I don't much care right now to find the right notation
        if key_file is not None:
            if isinstance(key,str):
                key_file=open(key,'r')
            key_head=key_file.readline()
            key_file.seek(0)
            if 'DSA' in key_head:
                keytype=paramiko.DSSKey
            elif 'RSA' in key_head:
                keytype=paramiko.RSAKey
            else:
                raise Exception("Can't identify key type")
            pkey=keytype.from_private_key(key_file)
            self.t.auth_publickey(username, pkey)
        else:
            if password is not None:
                self.t.auth_password(username,password,fallback=False)
            else: raise Exception('Must supply either key_file or password')
        self.sftp=paramiko.SFTPClient.from_transport(self.t)
        '''
        sclient = paramiko.SSHClient()
        sclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sclient.connect(hostname='192.168.0.202', username='paradigm',
                        password='rocketship')
        self.sftp = sclient.open_sftp()

    def command(self,cmd):
        #  Breaks the command by lines, sends and receives
        #  each line and its output separately
        #
        #  Returns the server response text as a string

        chan = self.t.open_session()
        chan.get_pty()
        chan.invoke_shell()
        chan.settimeout(20.0)
        ret=''
        try:
            ret+=chan.recv(1024)
        except:
            chan.send('\n')
            ret+=chan.recv(1024)
        for line in cmd.split('\n'):
            chan.send(line.strip() + '\n')
            ret+=chan.recv(1024)
        return ret

    def put(self,localfile,remotefile):
        #  Copy localfile to remotefile, overwriting or creating as needed.
        self.sftp.put(localfile,remotefile)

    def put_all(self,localpath,remotepath):
        #  recursively upload a full directory
        os.chdir(os.path.split(localpath)[0])
        parent=os.path.split(localpath)[1]
        for walker in os.walk(parent):
            try:
                self.sftp.mkdir(os.path.join(remotepath,walker[0]))
            except:
                pass
            for file in walker[2]:
                self.put(os.path.join(walker[0],file),os.path.join(remotepath,walker[0],file))

    def get(self,remotefile,localfile):
        #  Copy remotefile to localfile, overwriting or creating as needed.
        self.sftp.get(remotefile,localfile)

    def sftp_walk(self,remotepath):
        # Kindof a stripped down  version of os.walk, implemented for
        # sftp.  Tried running it flat without the yields, but it really
        # chokes on big directories.
        path=remotepath
        files=[]
        folders=[]
        for f in self.sftp.listdir_attr(remotepath):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        print (path,folders,files)
        yield path,folders,files
        for folder in folders:
            new_path=os.path.join(remotepath,folder)
            for x in self.sftp_walk(new_path):
                yield x

    def get_all(self,remotepath,localpath):
        #  recursively download a full directory
        #  Harder than it sounded at first, since paramiko won't walk
        #
        # For the record, something like this would gennerally be faster:
        # ssh user@host 'tar -cz /source/folder' | tar -xz

        self.sftp.chdir(os.path.split(remotepath)[0])
        parent=os.path.split(remotepath)[1]
        try:
            os.mkdir(localpath)
        except:
            pass
        for walker in self.sftp_walk(parent):
            try:
                os.mkdir(os.path.join(localpath,walker[0]))
            except:
                pass
            for file in walker[2]:
                self.get(os.path.join(walker[0],file),os.path.join(localpath,walker[0],file))
    def write_command(self,text,remotefile):
        #  Writes text to remotefile, and makes remotefile executable.
        #  This is perhaps a bit niche, but I was thinking I needed it.
        #  For the record, I was incorrect.
        self.sftp.open(remotefile,'w').write(text)
        self.sftp.chmod(remotefile,755)

import paramiko
import re
import os
import pandas as pd

# Even if there is only one file to send, the paths MUST be in a list for this function to work.
def sendfiles(sclient, localpaths, remotepaths):
    fclient = sclient.open_sftp()
    for i, path in enumerate(localpaths):
        fclient.put(path, remotepaths[i])
    fclient.close()


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
            text = re.sub(r'!(.*?)!', modrep, text)
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

    def testfunc(lookup):
        print(lookup)


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
    modparms.columns = modparms.loc['Key Value',:]
    modparms = modparms.drop('Key Value')
    return(modparms)

# The code below was used only for testing.


'''
inpdir = '/home/eric/projects/CityofLA_Opti/Input_Test/'
templatepath = '/home/eric/projects/CityofLA_Opti/Template_05-20-20.inp'
modparms_path = '/home/eric/projects/distributed-models/Wilmington_05-20-20_transposed (1).csv'




modparms = read_modparms(modparms_path)




runnames = modparms.index[1:]
runname = runnames[0]
for runname in runnames:
    keys = modparms.columns.astype(str)
    values = modparms.loc[runname, :]
    lookup = dict(zip(keys, values))
    lookup['OUTPATH'] = 'C:/SUSTAIN/Output/TempOut'
    inppath = os.path.join(inpdir, f'{runname}.inp')
    gen_inp(templatepath=templatepath, inppath=inppath, modrep=modrep, lookup=lookup, modpattern='!\d!')


modpattern = '!\d!'
with open(templatepath, 'r', encoding='utf_8') as template:
    with open(inppath, 'wt', encoding='utf_8', newline='\r\n') as output:
        text = template.read()
        text = re.sub(modpattern, modrep, text)
#            text = re.sub('?OUTPATH?', outpath, text)
        output.write(text)
template = open(templatepath, 'r', encoding='utf_8')
text = template.read()
re.sub(r'(?<=!).+?(?=!)', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',text)
text
re.match('', text)

lookup
inppath
gen_inp(templatepath, inppath, modrep, lookup, modpattern='!\d!')

modpattern = '!\d!'
batchpattern = '?\d?'

with open(templatepath, 'r', encoding='utf_8') as template:
    text = template.read()
    text = re.sub(pattern, repfunc, line)

re.sub(modpattern, lambda line: replace(line, suppress))
re.sub(modpattern, lambda text: replace(text, lookup))

re.sub('...     ', lambda line, suppress=suppress: replace(line, suppress))
re.sub(modpattern, lambda text, lookup=lookup: replace(text, lookup))



template = open(templatepath, 'r', encoding='utf_8')
template.read()
import re
text = template.read()

reptext = re.sub(pattern, repfunc, text)
reptext
pattern

test = pd.read_csv('~/Downloads/Wilmington_05-20-20_transposed.csv')
test = test.loc[:, ~test.columns.str.contains('^Unnamed')]
test = test.rename(columns={'Unnamed: 0':'Key Value'})

test.rename(columns=test['Key Value'])


gen_inp(templatepath=templatepath, pattern=pattern, modoutpattern = modoutpattern,
        repfunc=repfunc, lookup=lookup, outpath=newtemppath)
'''

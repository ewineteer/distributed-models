
# %%
import pandas as pd
import os
import tqdm

os.chdir('/home')

os.getcwd()

df = pd.read_csv('/home/eric/projects/InputData-WaterSupply_05-07-20.csv',header=None)
df = df[df.index != 1]
df = df[df.index != 2]
df = df.reset_index()
df.loc[0,pd.isna(df.loc[0,:])] = -1
reprows = df.iloc[0]
reprows = reprows.astype('int')
reprows = reprows.astype('str')



def gen_inp(template,reprows,repvals,filename):
    with open(filename, 'wt' ,encoding='utf_8') as fileout:
        for j,line in enumerate(template):
            row = str(j+1)
            if row in reprows.values:
                repind = reprows[reprows==row].index.astype(int)
                repval = repvals[repind+1]
                for val in repval:
                    line = line.replace('@',val,1)
            fileout.write(line)



batchfile = open('/home/eric/projects/wsmodrun.bat','w+' ,encoding='utf_8')

for i in tqdm.trange(1,len(df.index)):
    template = open('/home/eric/projects/Template.inp','r',encoding='utf_8')
    repvals = df.loc[i,].astype(str)
    origname = df.loc[i,5]
    filepath = '/home/eric/projects/Input/WS/'
    batchpath = 'C:/Projects/Input/WS/'
    filename = filepath + origname
    batchname = batchpath + origname
    gen_inp(template=template,reprows=reprows,repvals=repvals,filename=filename)
    batchfile.write("Sustain64.exe 2 " + batchname +'\n')


batchfile.write("pause\n")
batchfile.write("exit")
batchfile.close()

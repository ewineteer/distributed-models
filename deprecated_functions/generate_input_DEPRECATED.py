
# %%
import pandas as pd
import os
import tqdm

df = pd.read_csv('~/projects/CityofLA_Opti/OW-4_InputData-WaterQuality_05-19-20_v2.csv',header=None)
df = df[df.index != 1]
df = df[df.index != 2]
df = df.reset_index()
df.loc[0,pd.isna(df.loc[0,:])] = -1
reprows = df.iloc[0]
reprows = reprows.astype('int')
reprows = reprows.astype('str')



def gen_inp(template,reprows,repvals,filename):
    with open(filename, 'wt' ,encoding='utf_8', newline = '\r\n') as fileout:
        for j,line in enumerate(template):
            row = str(j+1)
            if row in reprows.values:
                repind = reprows[reprows==row].index.astype(int)
                repval = repvals[repind+1]
                for val in repval:
                    line = line.replace('@',val,1)
            fileout.write(line)



batchfile = open('/home/eric/projects/CityofLA_Opti/ow4_wqmodrun_V2.bat','w+' ,encoding='utf_8')

for i in tqdm.trange(1,len(df.index)):
    template = open('/home/eric/projects/CityofLA_Opti/OW-4_Template_05-19-20.inp','r',encoding='utf_8')
    repvals = df.loc[i,].astype(str)
    origname = df.loc[i,5]
    filepath = '/home/eric/projects/CityofLA_Opti/Input/OW_WQ_V2/'
    batchpath = 'C:/Projects/CityofLA_Opti/Input/WQ/'
    filename = filepath + origname
    batchname = batchpath + origname
    gen_inp(template=template,reprows=reprows,repvals=repvals,filename=filename)
    batchfile.write("Sustain64.exe 2 " + batchname +'\n')


batchfile.write("pause\n")
batchfile.write("exit")
batchfile.close()

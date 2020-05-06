
# %%
import pandas as pd
import os
import tqdm

df = pd.read_csv('C:/Users/Eric W/Downloads/InputData-Oakwood_Rustic_05-06-20.csv',header=None)
df = df[df.index != 1]
df = df[df.index != 2]
df = df.reset_index()
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




batchfile = open('C:/Users/Eric W/Downloads/modrun.bat','w+' ,encoding='utf_8')

for i in tqdm.trange(1,len(df.index)):
    template = open('C:/Users/Eric W/Downloads/Template.inp','r',encoding='utf_8')
    repvals = df.loc[i,].astype(str)
    filename = df.loc[i,5]
    filepath = 'C:/Projects/CityofLA_Opti/Input/WQ/'
    filename = filepath + filename
    gen_inp(template=template,reprows=reprows,repvals=repvals,filename=filename)
    batchfile.write("Sustain64.exe 2 " + filename +'\n')

batchfile.write("pause\n")
batchfile.write("exit")
batchfile.close()

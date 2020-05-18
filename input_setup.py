import pandas as pd
import os
import tqdm

df = pd.read_csv('~/projects/CityofLA_Opti/RC_InputData-WaterQuality_05-14-20.csv',header=None)
df = df[df.index != 1]
df = df[df.index != 2]
df = df.reset_index()
df.loc[0,pd.isna(df.loc[0,:])] = -1
reprows = df.iloc[0]
reprows = reprows.astype('int')
reprows = reprows.astype('str')


#This input generator is very brittle, and will hopefully be replaced soon with a much more flexible function.
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

def generate_log_file(path):



for i in tqdm.trange(1,len(df.index)):
    template = open('/home/eric/projects/CityofLA_Opti/RC_Template_05-14-20.inp','r',encoding='utf_8')
    repvals = df.loc[i,].astype(str)
    origname = df.loc[i,5]
    filepath = '/home/eric/projects/CityofLA_Opti/Input/RC_WQ/'
    filename = filepath + origname
    gen_inp(template=template,reprows=reprows,repvals=repvals,filename=filename)

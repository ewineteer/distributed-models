import os
import argparse
import sys
sys.path.append('/home/eric/projects/distributed-models')
import serverfuncs


parser = argparse.ArgumentParser()
parser.add_argument('temppath', type=str,
                    help='Path to input template.')
parser.add_argument('parmspath', type=str,
                    help='Path to model parameter lookup table.')
parser.add_argument('batchname', type=str,
                    help='The name of the batch run. This will be the name of the subfolder.')


args = parser.parse_args()
temppath = args.temppath
parmspath = args.parmspath
batchname = args.batchname

'''
temppath = '/home/eric/projects/CityofLA_Opti/Template_05-20-20.inp'
parmspath = '/home/eric/projects/distributed-models/Wilmington_05-20-20_transposed (1).csv'
batchname = 'testbatch'
'''


inpdir = '/home/eric/projects/distributed-models/Input/'

batchdir = os.path.join(inpdir, batchname)
if not os.path.exists(batchdir):
    os.makedirs(batchdir)

parms = serverfuncs.read_modparms(parmspath)
runnames = parms.index[1:]
runname = runnames[0]

for runname in runnames:
    keys = parms.columns.astype(str)
    values = parms.loc[runname, :]
    lookup = dict(zip(keys, values))
    lookup['OUTPATH'] = 'C:/SUSTAIN/Output/TempOut'
    repfunc = serverfuncs.RepFuncs()
    repfunc.lookup = lookup
    inppath = os.path.join(inpdir, batchname, f'{runname}.inp')
    serverfuncs.gen_inp(templatepath=temppath, inppath=inppath, modrep=repfunc.modrep)

print('Input files successfully generated.')

import glob
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('sustaindir', type=str,
                    help='The directory containing all SUSTAIN filse/folders.')
parser.add_argument('sustainver', type=str,
                    help='The version of SUSTAIN that will be checked.')
parser.add_argument('batchname', type=str,
                    help='The name of the batch run. This will be the name of the subfolder.')

args = parser.parse_args()
sustaindir = args.sustaindir
sustainver = args.sustainver
batchname = args.batchname


# Checks if the neccesary model executables exist. DOES NOT automatically install missing files.
def checkinstallation(sustaindir=sustaindir, sustainver=sustainver):
    checkpath = os.path.join(sustaindir, sustainver, '*')
    paths = glob.glob(checkpath)
    files = [os.path.basename(path) for path in paths]

    if 'VC_redist.x64.exe' not in files:
        print('WARNING - Missing visual C++ installer (it may still be installed, though.)')
    if 'sustain64.dll' not in files:
        print('WARNING - Missing SUSTAIN .dll file. SUSTAIN will not function without it.')
    if 'sustain64.exe' not in files:
        print('WARNING - Missing SUSTAIN executable. SUSTAIN will not function without it.')


# Creating the directories to check/create. This is only used if you call the function from command line.
tempindir = os.path.join(sustaindir, 'Input', 'TempIn')
tempoutdir = os.path.join(sustaindir, 'Output', 'TempOut')
batchindir = os.path.join(sustaindir, 'Input', batchname)
batchoutdir = os.path.join(sustaindir, 'Output', batchname)


# Place all directories that need to exist in a list and pass it to this function.
def makeinputdirs(directories=[sustaindir, tempindir, tempoutdir, batchindir, batchoutdir]):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


checkinstallation()
makeinputdirs()

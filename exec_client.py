import os
import subprocess
import glob

def runmodel(inputfile, sustainver):
    sustainexe = os.path.join('C:/SUSTAIN/', sustainver, 'sustain64.exe')
    sustaincommand = sustainexe + ' 2 ' + inputfile

def runallmodels(inputdir,sustainver):
    inpfiles = glob.glob(os.path.join(inputdir,'*.inp'))
    sustainexe = os.path.join('C:/SUSTAIN/', sustainver, 'sustain64.exe')
    for inpfile in inpfiles:
        subprocess.run([sustainexe, '2', inpfile])

runallmodels('C:/SUSTAIN/Input/cola-wilmington4', 'SUSTAIN-2.0')

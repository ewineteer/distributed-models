import os

def runmodel(input, sustainver):
    sustainexe = os.path.join('C:/SUSTAIN/', sustainver, 'sustain64.exe')
    print(sustainexe)


runmodel(input='nan', sustainver='SUSTAIN-2.0')

import argparse
import os
import glob

parser = argparse.ArgumentParser(description='File directories for model runs')
parser.add_argument('indir', type=str, help='Directory for input files.')
#parser.add_argument('sustain_executable', type=str, help='Path for sustain.exe.')

args = parser.parse_args()

print(args.indir)

inps = glob.glob(os.path.join(args.indir,'*'))

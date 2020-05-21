import re

def gen_inp(templatepath, pattern='!\d!', repfunc, lookup, inppath, outpath):
    with open(templatepath, 'r', encoding='utf_8') as template:
        with open(inppath, 'wt', encoding='utf_8', newline='\r\n') as output:
            for line in template:
                line = re.sub(pattern, repfunc, line)
                output.write(line)


def repfunc(match):
    string = match.group()
    repstring = re.sub('!', '', string)
    replacement = lookup.loc[lookup.orig == repstring, 'rep'].to_string(index=False).strip()
    return(replacement)


# The code below was used only for testing.
'''
import pandas as pd


newtemppath = '/home/eric/projects/CityofLA_Opti/new_temp_format_fill.inp'
templatepath = '/home/eric/projects/CityofLA_Opti/new_temp_format.inp'


lookup = pd.read_csv('/home/eric/projects/distributed-models/lookup.csv')
lookup['orig'] = lookup.orig.astype(str)
pattern = '!\d!'


gen_inp(templatepath=templatepath, pattern=pattern, repfunc=repfunc,
        lookup=lookup, outpath=newtemppath)
'''

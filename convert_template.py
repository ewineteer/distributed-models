
'''
This function converts our old legacy templates to the current one.
'''
def converttemp(oldtemppath,newtemppath):
    with open(oldtemppath, 'r', encoding = 'utf_8') as oldtemp:
        with open(newtemppath, 'wt' ,encoding='utf_8', newline = '\r\n') as newtemp:
            i = 1
            for line in oldtemp.readlines():
                if '@' in line:
                    j = 0
                    while j < len(line):
                        if line[j] == '@':
                            line = line[0:j] + f'!{i}!' + line[j+1:]
                            i += 1
                            j += 3
                        j += 1
                    newtemp.write(line)
                else:
                    newtemp.write(line)

'''
templates used for testing
oldtemppath = '/home/eric/projects/CityofLA_Opti/Template_05-13-20.inp'
newtemppath = '/home/eric/projects/CityofLA_Opti/new_temp_format.inp'
converttemp(oldtemppath,newtemppath)
'''

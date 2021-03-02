import os
print("Enter complete path of input directory")
path_of_input = input()
print("Enter complete path of output directory")
path_of_output = input()
f = open('.env', 'w')
f.write("PATH_OF_INPUT="+path_of_input+'\n')
f.write("PATH_OF_OUTPUT="+path_of_output)
f.close()
"""if not os.path.isdir(path_of_output+'/logs'):
    os.system("mkdir "+ path_of_output +"/logs")
if not os.path.isdir(path_of_output+'/number_of_lines'):
    os.system("mkdir "+path_of_output +"/number_of_lines")
"""
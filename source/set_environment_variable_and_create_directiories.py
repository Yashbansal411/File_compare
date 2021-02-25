import os
print("Enter the path of File_compare directory")
path_of_source = input()
f = open('.env', 'w')
f.write("PATH_OF_SOURCE="+path_of_source)
f.close()


if not os.path.isdir(path_of_source+'/output'):
    os.system("mkdir "+path_of_source+"/output")

if not os.path.isdir(path_of_source+'/output/logs'):
    os.system("mkdir "+ path_of_source +"/output/logs")

if not os.path.isdir(path_of_source+'/output/number_of_lines'):
    os.system("mkdir "+path_of_source +"/output/number_of_lines")

if not os.path.isdir(path_of_source+'/input'):
   os.system("mkdir "+path_of_source+"/input")


#/home/yash/new_file_compare/File_compare
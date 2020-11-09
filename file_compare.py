import linecache

def file_line_counter(file_path):
    count = 0
    with open(file_path,'r') as f:
        for line in f:
            count += 1
    f.close()
    return count


no_of_lines_file1 = file_line_counter('./file1.txt')
no_of_lines_file2 = file_line_counter('./file2.txt')

diff_in_line = (no_of_lines_file1-no_of_lines_file2)


with open('./output.txt','w') as f:
    diff = diff_in_line
    while(diff):
        f.write('<None>\n')
        diff -= 1
    f.close()

with open('./output.txt','a') as f:
    for i in range(1,no_of_lines_file2+1):
        string1 = linecache.getline('./file1.txt',(diff_in_line+i)).rstrip("\n")
        string2 = linecache.getline('./file2.txt',i).rstrip("\n")
        if string1 == string2:
            f.write(string1+'\n')
        else :
            f.write(string2+' <mismatch>'+'\n')
    f.close()

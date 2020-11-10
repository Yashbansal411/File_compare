def get_strings(file_name):
    list = []  # create empty list
    with open(file_name, 'r') as f:
        for line in f:
            list.append(line)
        f.close()
        return list

list1 = get_strings('./file1.txt')
list2 = get_strings('./file2.txt')
len = len(list2)
count = 0
with open('output.txt','w') as f:
    f.write('\n\n')
    for i in list2:
        count += 1
        if i in list1:
           f.write(i)
        else:
            if count == len:
                f.write(i.rstrip('\n') + '< Mismatched>')
            else:
                f.write(i.rstrip('\n') + '< Mismatched>'+ '\n\n\n')
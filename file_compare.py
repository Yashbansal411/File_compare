import linecache


def get_strings(file_name):
    list = []  # create empty list
    with open(file_name, 'r') as f:
        for line in f:
            list.append(line)
        f.close()
        return list


list1 = get_strings('./file1.txt')
list2 = get_strings('./file2.txt')

counter = 0
with open('./output.txt', 'w') as f:
    for i in list1:
        string = i.rstrip("\n")
        if i in list2 and counter == 0:  # when first match
            counter += 1
            list2.remove(i)
            f.write(string + '\n')
        elif i in list2:  # match
            f.write(string + '\n')
            list2.remove(i)
            counter += 1
        else:  # not a match at all
            if counter == 1:
                f.write('\n')

    for i in list2:
        i=i.rstrip('\n')
        f.write(i+' <mismatched>')
    f.close()

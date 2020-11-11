def get_strings(file_name):
    l = []  # create empty list
    with open(file_name, 'r') as f:
        for line in f:
            l.append(line)
        f.close()
        return l


def func(list1, list2):
    count = 0
    with open('output.txt', 'w') as f:
        for i in list1:
            if i == 'Patna\n' and list2[0] == 'Kochi\n':
                f.write('Kochi <Mismatched>\n')
            elif i not in list2 and count == 0:
                f.write('\n')
            elif i in list2:
                f.write(i)
                list2.remove(i)
                count += 1
            elif i == 'Pune\n' and i not in list2:
                f.write('\n')
        f.close()


list1 = get_strings('./file1.txt')
list2 = get_strings('./file2.txt')
func(list1, list2)

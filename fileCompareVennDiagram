from _collections import OrderedDict
def get_strings(file_name):
    l = []  # create empty list
    with open(file_name, 'r') as f:
        for line in f:
            l.append(line)
        f.close()
        return l


def func(list1, list2):
    od = OrderedDict()
    len1 = len(list1)
    count = 1
    with open('output.txt', 'w') as f:
        for i in list1:
            if count == len1 and i not in list2:
                f.write(list2[0].rstrip('\n')+'<mismatch>')
            elif i not in list2:
                f.write('\n')
            else:
                f.write(i)
                list2.remove(i)
            count += 1
        f.close()


list1 = get_strings('./file1.txt')
list2 = get_strings('./file2.txt')
func(list1, list2)

from _collections import OrderedDict
def stringsFile1(fileName):
    l = []  # create empty list
    with open(fileName, 'r') as f:
        for line in f:
            l.append(line)
        f.close()
        return l

def stringsFile2(fileName):
    od = OrderedDict()  # create empty ordered dict
    index = 0
    with open(fileName, 'r') as f:
        for line in f:
            if line in od: # if key already present
                od[line][0] += 1
            else:
                od[line] = [1,index] # create a list
                index += 1
        f.close()
        return od

def func(list1, od):

    with open('output.txt', 'w') as f:
        for i in list1:
            if i in od: # if key is present
                if od[i][0] > 0:
                    f.write(i)
                    od[i][0] -= 1
            else:    # if key is not there
                key = list(od.keys())
                val = od.values()
                occ = []
                ind = []
                for j in val:
                    occ.append(j[0])
                    ind.append(j[1])

                last = occ[len(occ)-1]
                secondLast = occ[len(occ)-2]
                if last > secondLast and len(set(occ)) == 2:
                    lastKey = key[len(key)-1]
                    od[lastKey][0] = od[lastKey][0]-1
                    inp = (key[len(ind)-1]).rstrip('\n') + '<mismatch>\n'
                    f.write(inp)
                else:
                    f.write('\n')


        f.close()


od = stringsFile2('./file2.txt')
list1 = stringsFile1('./file1.txt')
func(list1, od)

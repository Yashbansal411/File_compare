import time
def stringsFile1(fileName):
    l = []  # create empty list
    with open(fileName, 'r') as f:
        for line in f:
            l.append(line)
        f.close()
    return l

def func(list1,list2):
    list3 = ['\n']*(len(list1))
    List2Index = 0
    List2Length = len(list2)
    FirstMismatch = True
    LastIndexAdded = 0
    for i in list2:
        if i in list1: # check if element in file1
            index = list1.index(i)
            list3[index] = i
            list1[index] = i + 'processed'
            LastIndexAdded = index
        else: # executes when mismatch element is found
            if List2Index == List2Length - 1:
                if list3[len(list3)-1] == '\n':
                    list3[len(list3)-1] = i.rstrip('\n') + '<mismatch>\n'
                else:
                    list3.append(i.rstrip('\n')+'<mismatch>\n')
            else:
                if FirstMismatch:
                    try:
                        list3[LastIndexAdded+1] = i.rstrip('\n')+'<mismatch>\n'
                    except IndexError:
                        list3.append(i.rstrip('\n')+'<mismatch>\n')
                    LastIndexAdded += 1
                    FirstMismatch = False
                else:
                    if list3[len(list3) - 1] == '\n':
                        list2[List2Index - 1] = i.rstrip('\n') + '<mismatch>\n'
                    else:
                        list3.append(i.rstrip('\n') + '<mismatch>\n')
        List2Index += 1
        print(List2Index)
    return list3


def listToFile(list3):
    with open('output.txt','w') as f:
        for i in list3:
            f.write(i)
        f.close()

startTime = time.time()
list1 = stringsFile1('./file1.txt')
list2 = stringsFile1('./file2.txt')
list3 = func(list1,list2)
listToFile(list3)
endTime = time.time()
print("execution time= ", endTime-startTime)

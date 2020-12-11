import json
from operator import itemgetter
def inputToList(name):
    with open(name) as f:
        l = []
        for line in f:
            l.append(json.loads(line))
        return l
def myBinarySearch(list1, i):
    low = 0
    high = len(list1)-1
    first_occurrence = -1
    while(low <= high):
        mid = low + int((high-low)/2)
        if(list1[mid]['raw_log_time']==i['raw_log_time']): # if raw_log_time is same
             first_occurrence = mid
             high = mid - 1
        else:
            if(list1[mid]['raw_log_time']>i['raw_log_time']):
                high = mid - 1
            else:
                low = mid + 1
    return first_occurrence


def processMisMatch(list2,list3,list2Index,i,lastAppend):
    if (list2Index == len(list2) - 1):  # if we encounter last element of list2

        if (list3[len(list3) - 1] == '\n'):  # if in list3 last value blank then push the o/p there
            list3[len(list3) - 1] = str(i) + '<mismatch>'
        else:
            list3.append(str(i) + '<mismatch>')

    else:
        try:
            list3[lastAppend + 1] = str(i) + '<mismatch>'
        except IndexError:
            list3.append(str(i) + '<mismatch>')
        lastAppend += 1
    return lastAppend


def mainFunc(list1, list2):
    list3 = ['\n']*len(list1)
    list2Index = 0
    lastAppend = -1
    for i in list2:
        index = myBinarySearch(list1,i)
        if index == -1: #check that index is valid or not, if index = -1 then there is no match for for raw-log_time.
            lastAppend=processMisMatch(list2, list3, list2Index, i, lastAppend)

        else: #either we got first occurrence or the exact matc
            indexFound = False #initiall we assume that we don't get the exact match
            while(index<len(list1)): #apply linear search and find the exact dict
                    if(list1[index]['raw_log_time']!=i['raw_log_time']):#if we didn't get the same time that means form now onward there is no chance to get exact same dict
                        break
                    else:
                        if(list1[index] == i): #if got same dict then just put it at right place, change value of indexfound and break the loop to save time.
                            list3[index] = i
                            lastAppend = index
                            indexFound = True
                            list1[index]['id'] = 'processed'
                            break
                        else:
                            index += 1

            if(indexFound==False): #if indexfound is still false that means there is no exact match so we need to process the mismatch
                    lastAppend = processMisMatch(list2, list3, list2Index, i, lastAppend)

        list2Index += 1
    return list3

def listToFile(list3):
    with open('output_50L.txt','w') as f:
        for i in list3:
            i = str(i)
            i = i.replace(" ","")
            if i != '\n':
                i = i+'\n'
            f.write(i)
        f.close()


list1 = inputToList("file1_50L.txt")
list2 = inputToList('file2_50L.txt')
#sorted_list=sorted(l,key=lambda i:i["raw_log_time"])
sorted_list1 = sorted(list1, key=itemgetter('raw_log_time'))
list3 = mainFunc(sorted_list1, list2)
listToFile(list3)
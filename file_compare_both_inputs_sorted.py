from operator import itemgetter
import json


def inputToList(name):
    with open(name) as f:
        l = []
        for line in f:
            l.append(json.loads(line))
        return l


def adjust_mismatch(list2,list3,list2Index,i,lastAppend):
    if (list2Index == len(list2) - 1):  # if we encounter last element of list2

        if (list3[len(list3) - 1] == '\n'):  # if in list3 last value blank then push the o/p there
            list3[len(list3) - 1] = str(i) + '<mismatch>'
        else:
            list3.append(str(i) + '<mismatch>')

    else:
        while(True):
            if lastAppend == (len(list3)-1):
                list3.append(str(i) + '<mismatch>')
                lastAppend += 1
                break
            if list3[lastAppend+1] == '\n':
                list3[lastAppend + 1] = str(i) + '<mismatch>'
                lastAppend += 1
                break
            lastAppend += 1





def main_func(list1, list2):
    last_checked_index = -1
    list1_len = len(list1)
    list2_index = 0
    list3 = ['\n']*len(list1) # create a list of same len as list1
    for second in list2:
        second_unprocessed = True #if there is inputs left in list2 and there is no unprocessed left input1 then we can't enter in  upcoming loop
        for first in range(last_checked_index+1, list1_len):# as both the inputs are sorted, we don't need to check for already checked inputs
            second_unprocessed = False # if we enter inside the loop then we don't need to prcess it explicitly.
            if list1[first]['id'] < second['id']:
                continue

            if list1[first]['id'] > second['id']: # no match is possible, append mismatch
                adjust_mismatch(list2,list3,list2_index,second,last_checked_index)
                break

            else:  # id must be equal
                if list1[first] == second: #check that both the input is equal
                    list3[first] = second
                    last_checked_index = first
                    break
                else : #if there is any mismatch field in other than ids
                    adjust_mismatch(list2,list3,list2_index,second,last_checked_index)
        if(second_unprocessed==True):
            adjust_mismatch(list2,list3,list2_index,second,last_checked_index)
        list2_index += 1
    return list3

def listtofile(list3):
    with open('Testingfiles/output_50L.txt','w') as f:
        for i in list3:
            i = str(i)
            i = i.replace(" ","")
            if i != '\n':
                i = i+'\n'
            f.write(i)


list1 = inputToList('Testingfiles/file1_50L.txt') #1L 2000 sec.
list2 = inputToList('Testingfiles/file2_50L.txt')
sorted_list1 = sorted(list1, key=itemgetter('id'))
sorted_list2 = sorted(list2, key=itemgetter('id'))
list3 = main_func(sorted_list1, sorted_list2)
listtofile(list3)
print("complete")

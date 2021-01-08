from operator import itemgetter
import json
import time


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


def core_logic(list1, list2):
    list3 = ['\n']*len(list1)
    list1_len = len(list1)
    first_occur = 0
    list2_index = 0
    last_append = 0
    for second in list2:
        second_unprocessed = True
        for first in range(first_occur, list1_len):
            if second["raw_log_time"] < list1[first]["raw_log_time"]:
                break
            else:
                if list1[first]["raw_log_time"] > list1[first_occur]["raw_log_time"]:
                    first_occur = first
                if list1[first] == second:
                    list3[first] = second
                    second_unprocessed = False
                    last_append = first
                    list1[first]["id"] = "processed"
                    break
        if second_unprocessed:
            adjust_mismatch(list2, list3, list2_index, second, last_append)
        list2_index += 1
    return list3

def input_to_list(name):
    with open(name) as f:
        l = []
        for line in f:
            l.append(json.loads(line))
        return l


def list_to_file(list3,code):
    with open('output_files/'+code+'.txt','w') as f:
        for i in list3:
            i = str(i)
            i = i.replace(" ","")
            if i != '\n':
                i = i+'\n'
            f.write(i)


def main_code(file1_address, file2_address):
    list1 = input_to_list(file1_address) #1L 2000 sec.
    list2 = input_to_list(file2_address)
    sorted_list1 = sorted(list1, key=itemgetter('raw_log_time'))
    sorted_list2 = sorted(list2, key=itemgetter('raw_log_time'))
    list3 = core_logic(sorted_list1, sorted_list2)
    #list_to_file(list3)
    return list3


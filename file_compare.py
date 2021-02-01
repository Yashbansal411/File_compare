import pandas as pd
import numpy as np
import os
import json
total_threads = 0

def read_input(file1_address, file2_address):
    df1_from_txt = pd.read_csv(file1_address, header=None, delimiter=":")
    df2_from_txt = pd.read_csv(file2_address, header=None, delimiter=":")
    df1_from_txt[["time", "raw"]] = df1_from_txt[6].str.split(',', expand=True)
    df2_from_txt[["time", "raw"]] = df1_from_txt[6].str.split(',', expand=True)
    ans1 = df1_from_txt.astype(dtype='int32', errors='ignore')
    del (df1_from_txt)
    ans2 = df2_from_txt.astype(dtype='int32', errors='ignore')
    del(df2_from_txt)
    ans1.sort_values(by='time', inplace=True)
    narr1 = ans1.to_numpy()
    del (ans1)
    ans2.sort_values(by='time', inplace=True)
    narr2 = ans2.to_numpy()
    del (ans2)
    return narr1, narr2


def core_logic(list1,list1_time,list2, list2_time):
    list3 = ['\n']*len(list1)
    list1_len = len(list1)
    first_occur = 0
    list2_index = 0
    last_append = 0
    for second in list2_time:
        second_unprocessed = True
        for first in range(first_occur, list1_len):
            if second < list1_time[first]:
                break
            else:
                if list1_time[first] > list1_time[first_occur]:
                    first_occur = first
                if(list1[first] == list2[list2_index]):                                    #np.array_equal(list1[first],second):
                    ans_str = str(list1[first])
                    list3[first] = ans_str
                    second_unprocessed = False
                    last_append = first
                    list1[first][0] = "processed"
                    break
        if second_unprocessed:
            adjust_mismatch(list2, list3, list2_index, list2[list2_index], last_append)
        list2_index += 1
        print(list2_index)
    return list3


def adjust_mismatch(list2, list3, list2Index, second, lastAppend):
    if (list2Index == len(list2) - 1):  # if we encounter last element of list2

        if list3[len(list3)-1] == '\n':  # if in list3 last value blank then push the o/p there
            ans_str = str(second)
            list3[len(list3) - 1] = ans_str + '<mismatch>'
        else:
            #ans = np.delete(second, np.s_[23:26])
            ans_str = str(second)
            list3.append(ans_str + '<mismatch>')

    else:
        while(True):
            if lastAppend == (len(list3)-1):
                #ans = np.delete(second, np.s_[23:26])
                ans_str = str(second)
                list3.append(ans_str + '<mismatch>')
                lastAppend += 1
                break
            if list3[lastAppend] == '\n':
                #ans = np.delete(second, np.s_[23:26])
                ans_str = str(second)
                list3[lastAppend] = ans_str + '<mismatch>'
                lastAppend += 1
                break
            lastAppend += 1


def list_to_file(list3,code):
    with open('output_files/'+code+'.txt','w') as f:
        for i in list3:
            i = i.replace('\n', '')
            i = i.replace('[', '')
            i = i.replace(']', '')
            i = i.replace("\'", '')
            i = i.replace(",  ", ":")
            i = i.replace(" ", "")
            if i != '\n':
                i = i+'\n'
            f.write(i)


def persist_file_length(list3, code):
    total_number_of_lines = len(list3)
    with open("number_of_lines.txt") as f:
        ans = ''
        for i in f:
            ans = ans + str(i)
        if os.stat("number_of_lines.txt").st_size == 0:
            js = {}
            js[code] = total_number_of_lines
        else:
            js = json.loads(ans)
            js[str(code)] = total_number_of_lines
    f = open("number_of_lines.txt", 'w')
    f.write(str(js).replace("'", '"'))
    f.close()


def main_code(file1_address, file2_address,code):
    global total_threads
    total_threads += 1
    narr1, narr2 = read_input(file1_address, file2_address)
    narr1_time = narr1[:, 23]
    narr2_time = narr2[:, 23]
    narr1 = np.delete(narr1, np.s_[23:26], 1)
    narr2 = np.delete(narr2, np.s_[23:26], 1)
    narr1 = narr1.tolist()
    narr2 = narr2.tolist()
    list3 = core_logic(narr1,narr1_time, narr2, narr2_time)
    list_to_file(list3, code)
    persist_file_length(list3, code)
    total_threads -= 1


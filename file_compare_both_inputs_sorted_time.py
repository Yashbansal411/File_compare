import json, pandas as pd , numpy as np
import time


def adjust_mismatch(list2,list3,list2Index,second,lastAppend):
    if (list2Index == len(list2) - 1):  # if we encounter last element of list2

        if list3[len(list3)-1] == '\n':  # if in list3 last value blank then push the o/p there
            ans = np.delete(second, np.s_[23:26])
            ans_str = str(ans)
            list3[len(list3) - 1] = ans_str + '<mismatch>'
        else:
            ans = np.delete(second, np.s_[23:26])
            ans_str = str(ans)
            list3.append(ans_str + '<mismatch>')

    else:
        while(True):
            if lastAppend == (len(list3)-1):
                ans = np.delete(second, np.s_[23:26])
                ans_str = str(ans)
                list3.append(ans_str + '<mismatch>')
                lastAppend += 1
                break
            if list3[lastAppend] == '\n':
                ans = np.delete(second, np.s_[23:26])
                ans_str = str(ans)
                list3[lastAppend] = ans_str + '<mismatch>'
                lastAppend += 1
                break
            lastAppend += 1


def core_logic(list1, list2):
    list3 = ['\n'] * len(list1)
    list1_len = len(list1)
    first_occur = 0
    list2_index = 0
    last_append = 0
    for second in list2:
        second_unprocessed = True
        for first in range(first_occur, list1_len):
            if second[23] < list1[first][23]:
                break
            else:
                if list1[first][23] > list1[first_occur][23]:
                    first_occur = first
                if np.array_equal(list1[first], second):
                    ans = np.delete(second, np.s_[23:26])
                    ans_str = str(ans)
                    list3[first] = ans_str
                    second_unprocessed = False
                    last_append = first
                    list1[first][0] = "processed"
                    break
        if second_unprocessed:
            adjust_mismatch(list2, list3, list2_index, second, last_append)
        list2_index += 1
        print(list2_index)
    return list3


def list_to_file(list3,code):
    with open('output_files/'+code+'.txt','w') as f:
        for i in list3:
            i = str(i)
            i = i.replace('\n', '')
            i = i.replace('[', '')
            i = i.replace(']', '')
            i = i.replace("\'", '')
            i = i.replace("  ", ":")
            i = i.replace(" ", "")
            if i != '\n':
                i = i+'\n'
            f.write(i)


def read_input(file_name1, file_name2):
    df1_from_txt = pd.read_csv(file_name1, header=None, delimiter=":")
    df2_from_txt = pd.read_csv(file_name2, header=None, delimiter=":")
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


def main_code(file1_address, file2_address):
    sorted_list1, sorted_list2 = read_input(file1_address, file2_address)
    list3 = core_logic(sorted_list1, sorted_list2)
    return list3


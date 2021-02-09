import pandas as pd
import os
import json
from operator import itemgetter
total_threads = 0

main_keys = ['id', 'e_type', 'source', 'vendor', 'time', 'raw_log_time', 'evt_order', 'fields']
field_keys = ['table_name', '-msg-type', 'host', 'db_operation', 'src_ip', 'dest_host', 'database_name', 'app', 'time', 'error_code', 'user', 'db_query']


def read_input(file_address):
    df1 = pd.read_json(file_address, orient='records', lines=True, chunksize=10000)
    try:
        input1 = df1.read()
    except ValueError:
        return -1
    dict1 = input1.to_dict('records')
    for i in dict1:
        if list(i.keys()) != main_keys or list(i['fields'].keys()) != field_keys:
            return -2
    del input1
    return dict1


def core_logic(list1, list2):
    list3 = ['\n'] * len(list1)
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
        print(list2_index)
    return list3


def adjust_mismatch(list2, list3, list2Index, second, lastAppend):
    if (list2Index == len(list2) - 1):  # if we encounter last element of list2

        if list3[len(list3)-1] == '\n':  # if in list3 last value blank then push the o/p there
            ans_str = str(second)
            list3[len(list3) - 1] = ans_str + '<mismatch>'
        else:
            ans_str = str(second)
            list3.append(ans_str + '<mismatch>')

    else:
        while(True):
            if lastAppend == (len(list3)-1):
                ans_str = str(second)
                list3.append(ans_str + '<mismatch>')
                lastAppend += 1
                break
            if list3[lastAppend] == '\n':
                ans_str = str(second)
                list3[lastAppend] = ans_str + '<mismatch>'
                lastAppend += 1
                break
            lastAppend += 1


def list_to_file(list3, code):
    if not os.path.isdir('./output_files'):
        os.mkdir('./output_files')
    if isinstance(list3, str):
        f = open('output_files/'+code+'.txt', 'w')
        f.write(list3)
    else:
        with open('output_files/'+code+'.txt','w') as f:
            for i in list3:
                i = str(i)
                i = i.replace(" ", "")
                if i != '\n':
                    i = i+'\n'
                f.write(i)


def persist_file_length(list3, code):
    if isinstance(list3, str):
        total_number_of_lines = 1
    else:
        total_number_of_lines = len(list3)
    with open("number_of_lines.txt") as f:
        ans = ''
        for i in f:
            ans = ans + str(i)
        if os.stat("number_of_lines.txt").st_size == 0:
            js={}
            js[code] = total_number_of_lines
        else:
            js = json.loads(ans)
            js[str(code)] = total_number_of_lines
    f = open("number_of_lines.txt", 'w')
    f.write(str(js).replace("'", '"'))
    f.close()


def main_code(file1_address, file2_address, code):
    global total_threads
    total_threads += 1
    list1 = read_input(file1_address)
    list2 = read_input(file2_address)
    if isinstance(list1, int) or isinstance(list2, int): # check if any inputs are not in json or key missing
        if list1 == -1 and list2 == -1:
            list3 = 'both inputs are not in proper json format'
        elif list1 == -2 and list2 == -2:
            list3 = 'keys are missing from both input files'
        elif list1 == -1:
            list3 = 'file1 not in proper json format'
        elif list2 == -1:
            list3 = 'file2 not in proper json format'
        elif list1 == -2:
            list3 = 'keys from file1 are missing'
        elif list2 == -2:
            list3 = 'keys from file2 are missing'
    else:
        sorted_list1 = sorted(list1, key=itemgetter('raw_log_time'))
        sorted_list2 = sorted(list2, key=itemgetter('raw_log_time'))
        list3 = core_logic(sorted_list1, sorted_list2)
    list_to_file(list3, code)
    persist_file_length(list3, code)
    total_threads -= 1

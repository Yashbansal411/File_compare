import pandas as pd
import os
import json
from operator import itemgetter
import shutil
total_threads = 0


def read_input(file_address):
    df1 = pd.read_json(file_address, orient='records', lines=True, chunksize=10000)
    try:
        input1 = df1.read()
    except ValueError:
        return -1
    dict1 = input1.to_dict('records')
    del input1
    return dict1


def sort_input(input_list):
    try:
        sorted_list = sorted(input_list, key=itemgetter('raw_log_time'))
    except KeyError:
        return -1
    else:
        return sorted_list


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
            last_append = adjust_mismatch(list2, list3, list2_index, second, last_append)
        list2_index += 1
        print(list2_index)
    return list3


def adjust_mismatch(list2, list3, list2_index, second, last_append):
    if (list2_index == len(list2) - 1):  # if we encounter last element of list2

        if list3[len(list3) - 1] == '\n':  # if in list3 last value blank then push the o/p there
            ans_str = str(second)
            list3[len(list3) - 1] = ans_str + '<mismatch>'
        else:
            ans_str = str(second)
            list3.append(ans_str + '<mismatch>')

    else:
        while True:
            if last_append == (len(list3) - 1):
                ans_str = str(second)
                list3.append(ans_str + '<mismatch>')
                last_append += 1
                break
            if list3[last_append] == '\n':
                ans_str = str(second)
                list3[last_append] = ans_str + '<mismatch>'
                last_append += 1
                break
            last_append += 1
    return last_append


def list_to_file(list3, code):
    #if not os.path.isdir('output'):
    #    os.mkdir('output')
    if isinstance(list3, str): # execute when there is an error in inputs
        f = open('output/' + code + '.txt', 'w')
        f.write(list3)
        return list3
    total_free_space_in_mb = shutil.disk_usage('.').free / 1000000
    if total_free_space_in_mb < 1200:
        list3 = "No sufficient space in directory"
        f = open('output/' + code + '.txt', 'w')
        f.write(list3)
        return list3
    else:
        with open('output/' + code + '.txt', 'w') as f:
            for i in list3:
                i = str(i)
                i = i.replace(" ", "")
                if i != '\n':
                    i = i + '\n'
                f.write(i)
    return list3


def persist_file_length(list3, code):
    if not os.path.exists('number_of_lines/number_of_lines.txt'):
        os.system("touch number_of_lines/number_of_lines.txt")
    if isinstance(list3, str):
        total_number_of_lines = 1
    else:
        total_number_of_lines = len(list3)
    with open("number_of_lines/number_of_lines.txt") as f:
        ans = ''
        for i in f:
            ans = ans + str(i)
        if os.stat("number_of_lines/number_of_lines.txt").st_size == 0:
            js = {}
            js[code] = total_number_of_lines
        else:
            js = json.loads(ans)
            js[str(code)] = total_number_of_lines
    f = open("number_of_lines/number_of_lines.txt", 'w')
    f.write(str(js).replace("'", '"'))
    f.close()


def main_code(file1_address, file2_address, code):
    global total_threads
    total_threads += 1
    list1 = read_input(file1_address)
    list2 = read_input(file2_address)
    if isinstance(list1, int) or isinstance(list2, int):  # check if any inputs are not in json or key missing
        if list1 == -1 and list2 == -1:
            list3 = 'both inputs are not in proper json format'
        elif list1 == -1:
            list3 = 'file1 not in proper json format'
        elif list2 == -1:
            list3 = 'file2 not in proper json format'
    else:
        sorted_list1 = sort_input(list1)
        sorted_list2 = sort_input(list2)
        if isinstance(sorted_list1, int) or isinstance(sorted_list2, int):
            if sorted_list1 == -1 and sorted_list2 == -1:
                list3 = 'raw_log_time missing from both input'
            elif sorted_list1 == -1:
                list3 = 'raw_log_time missing from file1'
            elif sorted_list2 == -2:
                list3 = 'raw_log_time missing from file2'
        else:
            list3 = core_logic(sorted_list1, sorted_list2)
    list3 = list_to_file(list3, code)
    persist_file_length(list3, code)
    total_threads -= 1

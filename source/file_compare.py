from itertools import chain
from linecache import getline
import pandas as pd
import os
import json
from operator import itemgetter
import shutil
import ast
import math
import logging

total_threads = 0


def replace_single_quotes_with_double_quotes(file_address):
    temp_file = open("input/temp_file.txt", 'w')
    logging.info("inside single quotes function")
    with open(file_address) as main_file:
        for line in main_file:
            line = line.replace("'", '"')
            try:
                line = str(ast.literal_eval(line))
            except (SyntaxError, ValueError):
                continue
            line = line.replace("'", '"')
            temp_file.write(line + '\n')
    temp_file.close()
    os.remove(file_address)
    logging.info("got correct input files")
    os.rename("input/temp_file.txt", file_address)


def read_input_json(file_address):
    df1 = pd.read_json(file_address, orient='records', lines=True, chunksize=10000)
    logging.info("object created")
    try:
        input1 = df1.read()
        logging.info("dataframe created")
    except ValueError:  # if raise error then try to convert single_quotes to double quotes
        replace_single_quotes_with_double_quotes(file_address)
        df1 = pd.read_json(file_address, orient='records', lines=True, chunksize=10000)
        try:
            input1 = df1.read()
        except ValueError:
            return "input was not in proper json format"
    dict1 = input1.to_dict('records')
    logging.info("list of dictionary created")
    """if input1.isnull().T.any().T.sum() > 0:  # if key was missing from input than expression will return integer > 0
        return "key was missing from input"""
    del input1
    logging.info("data frame deleted")
    return dict1


def read_input_text(file_address):
    object1 = pd.read_csv(file_address, sep='\n', header=None, iterator=True)
    data_frame1 = object1.read()
    list1 = data_frame1.values.tolist()
    del data_frame1
    sorted_list = sorted(list1, key=lambda l: l[0])
    list2 = list(chain.from_iterable(sorted_list))
    del sorted_list
    return list2


def sort_input_json(input_list):
    # first check if value of raw_log_time key is none or not
    logging.info("check for missing raw")
    for i in input_list:
        try:
            if math.isnan(i["raw_log_time"]):
                return None
        except KeyError:
            return None
    logging.info("working on sorting")
    sorted_list = sorted(input_list, key=itemgetter('raw_log_time'))
    logging.info("sorting done")
    return sorted_list


def core_logic_text(list1, list2):
    list3 = ['\n'] * len(list1)
    list1_len = len(list1)
    first_occur = 0
    list2_index = 0
    last_append = 0
    for second in list2:
        second_unprocessed = True
        for first in range(first_occur, list1_len):
            if list1[first] == "already_processed":
                continue
            if second < list1[first]:
                break
            else:
                if list1[first] > list1[first_occur]:
                    first_occur = first
                if list1[first] == second:
                    list3[first] = second
                    second_unprocessed = False
                    last_append = first
                    list1[first] = "already_processed"
                    break
        if second_unprocessed:
            last_append = adjust_mismatch(list2, list3, list2_index, second, last_append)
        list2_index += 1
        #print(list2_index)
    return list3


def core_logic_json(list1, list2):
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
    if list2_index == len(list2) - 1:  # if we encounter last element of list2

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
    if not os.path.isdir('output'):
        os.system('mkdir output')
    if isinstance(list3, str):  # execute when there is an error in inputs
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
    if not os.path.isdir('output'):
        os.system('mkdir output')
    if not os.path.isdir('output/number_of_lines'):
        os.system('mkdir output/number_of_lines')
    if not os.path.exists('output/number_of_lines/number_of_lines.txt'):
        os.system("touch output/number_of_lines/number_of_lines.txt")
    if isinstance(list3, int):
        total_number_of_lines = list3
    elif isinstance(list3, str):
        total_number_of_lines = 1
    else:
        total_number_of_lines = len(list3)
    with open("output/number_of_lines/number_of_lines.txt") as f:
        ans = ''
        for i in f:
            ans = ans + str(i)
        if os.stat("output/number_of_lines/number_of_lines.txt").st_size == 0:
            js = {code: total_number_of_lines}
        else:
            js = json.loads(ans)
            js[str(code)] = total_number_of_lines
    f = open("output/number_of_lines/number_of_lines.txt", 'w')
    f.write(str(js).replace("'", '"'))
    f.close()


def for_json_only(file1_address, file2_address, code):
    logging.info("entered inside for json only")
    list1 = read_input_json(file1_address)
    list2 = read_input_json(file2_address)
    if isinstance(list1, str) or isinstance(list2, str):
        if list1 == "input was not in proper json format" and list2 == "input was not in proper json format":
            list3 = 'both inputs are not in proper json format'
        elif list1 == "input was not in proper json format":
            list3 = 'file1 not in proper json format'
        elif list2 == "input was not in proper json format":
            list3 = 'file2 not in proper json format'
        """elif list1 == "key was missing from input" and list2 == "key was missing from input":
            list3 = "Key was missing from both input files"
        elif list1 == "key was missing from input":
            list3 = "Key was missing from file1"
        elif list2 == "key was missing from input":
            list3 = "Key was missing from file2"""
    else:
        sorted_list1 = sort_input_json(list1)
        sorted_list2 = sort_input_json(list2)
        if sorted_list1 is None and sorted_list2 is None:
            list3 = 'raw_log_time missing from both input'
        elif sorted_list1 is None:
            list3 = 'raw_log_time missing from file1'
        elif sorted_list2 is None:
            list3 = 'raw_log_time missing from file2'
        else:
            list3 = core_logic_json(sorted_list1, sorted_list2)
    list3 = list_to_file(list3, code)
    persist_file_length(list3, code)


def for_text_only(file1_address, file2_address, code):
    sorted_list1 = read_input_text(file1_address)
    sorted_list2 = read_input_text(file2_address)
    list3 = core_logic_text(sorted_list1, sorted_list2)
    list3 = list_to_file(list3, code)
    persist_file_length(list3, code)


def main_code(file1_address, file2_address, code):
    global total_threads
    total_threads += 1
    logging.info("entered inside main function")
    is_text = False
    for i in range(5):
        if is_text:
            break
        line1 = getline(file1_address, i + 1)
        line2 = getline(file2_address, i + 1)
        if line1 == '' or line1 == '\n' or line1[0] != '{' or line1[-2] != '}':
            is_text = True
        if line2 == '' or line2 == '\n' or line2[0] != '{' or line2[-2] != '}':
            is_text = True
    if is_text is True:
        for_text_only(file1_address, file2_address, code)
    else:
        for_json_only(file1_address, file2_address, code)
    total_threads -= 1
    return is_text

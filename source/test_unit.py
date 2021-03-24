import os

os.system("mkdir output")
os.system("mkdir output/logs")
import pytest
import file_compare as file
import flask_file_compare as flask_code
import json


# to run this file use command python3 -m pytest test_unit.py

def test_exact_same():
    list1 = [{"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "334l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list2 = [{"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "334l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list3 = file.core_logic_json(list1, list2)
    assert list3 == [{'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '334l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}]

    list1 = ["Delhi", "Mumbai", "Pune"]
    list2 = ["Delhi", "Mumbai", "Pune"]
    list3 = file.core_logic_text(list1, list2)
    assert list3 == ["Delhi", "Mumbai", "Pune"]


def test_exact_same_list1_greater():
    list1 = [{"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "334l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "335l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list2 = [{"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "334l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list3 = file.core_logic_json(list1, list2)
    assert list3 == [{'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '334l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     '\n']

    list1 = ["Delhi", "Mumbai", "Pune", "kochi", "Banglore"]
    list2 = ["Delhi", "Mumbai", "Pune"]
    list3 = file.core_logic_text(list1, list2)
    assert list3 == ["Delhi", "Mumbai", "Pune", '\n', '\n']

    list1 = ["Delhi", "Mumbai", "Pune", "kochi", "Banglore"]
    list1.sort()
    list2 = ["Delhi", "Mumbai", "Banglore"]
    list2.sort()
    list3 = file.core_logic_text(list1, list2)
    assert list3 == ['Banglore', 'Delhi', 'Mumbai', '\n', '\n']


def test_exact_same_list2_greater():
    list1 = [{"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "334l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "335l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list2 = [{"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "334l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "335l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "336l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]  # extra input at last index

    list3 = file.core_logic_json(list1, list2)
    assert list3 == [{'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '334l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '335l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     "{'id': '336l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}<mismatch>"]

    list1 = ["Delhi", "Mumbai", "Bangalore"]
    list2 = ["Delhi", "Mumbai", "Pune", "Kochi", "Bangalore"]
    list1.sort()
    list2.sort()
    list3 = file.core_logic_text(list1, list2)
    assert list3 == ['Bangalore', 'Delhi', 'Mumbai', 'Kochi<mismatch>', 'Pune<mismatch>']


def test_differ():
    list1 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "338l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list2 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "338l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "343l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]  # different id at last index

    list3 = file.core_logic_json(list1, list2)
    assert list3 == [{'id': '323l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     '\n',
                     {'id': '338l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     "{'id': '343l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}<mismatch>"]

    list2 = ["Delhi", "Mumbai", "Kochi", "Kochi2", "Kochi3"]
    list1 = ["Delhi", "Mumbai", "Maharashtra", "Pune", "Kochi"]
    list1.sort()
    list2.sort()
    list3 = file.core_logic_text(list1, list2)
    assert list3 == ['Delhi', 'Kochi', 'Kochi2<mismatch>', 'Mumbai', '\n']


def test_duplicate():
    list1 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             ]

    list2 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list3 = file.core_logic_json(list1, list2)
    assert list3 == [{'id': '323l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     "{'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}<mismatch>"]

    list2 = ["Delhi", "Delhi", "Delhi"]
    list1 = ["Delhi", "Delhi"]
    list1.sort()
    list2.sort()
    list3 = file.core_logic_text(list1, list2)
    assert list3 == ['Delhi', 'Delhi', 'Delhi<mismatch>']


def test_extra_spaces_between_keys_value_pair():
    # test to check if code can handle extra space between key value pairs
    list1 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},  # extra space b/w id and raw_log_time
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},  # extra space b/w raw_time and evt_order
             ]

    list2 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             ]
    list3 = file.core_logic_json(list1, list2)
    assert list3 == [{'id': '323l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}]


def test_extra_space_between_key_and_value():
    # to check if code can handle extra spaces between key and value
    list1 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},  # extra space between 'id' and 323l
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             # extra space between 'raw_log_time' and 8
             ]

    list2 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},  # extra space between "user" and "abc"
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             ]
    list3 = file.core_logic_json(list1, list2)
    assert list3 == [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
                     {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
                     ]


# testing flask code
def test_no_body_file_compare():
    # to check body is empty or not

    client = flask_code.application.test_client()
    url = '/file_compare/'
    json_input = ''
    response = client.post(url, data=json_input)
    assert response.status_code == 500 and response.get_data() == b'please enter the input body, body is empty'


def test_input_body_in_json_file_compare():
    # to check both body is not in proper json format
    client = flask_code.application.test_client()
    url = '/file_compare/'
    json_input = '{"file1_address"="test/file1_10.txt", "file2_address": "test/file2_10.txt"}'  # '=' between key and value
    response = client.post(url, data=json_input)
    assert response.status_code == 500 and response.get_data() == b'input not in proper format, input must be a json'


def test_file_address_key_is_present():
    # check if necessary keys present in body or not
    client = flask_code.application.test_client()
    url = '/file_compare/'
    json_input2 = {"file_add": "test/file1.txt", "file1_add": "test/file2.txt"}
    response2 = client.post(url, data=json.dumps(json_input2))
    json_input3 = {"file2_address": "file2_10000.txt"}
    response3 = client.post(url, data=json.dumps(json_input3))
    json_input4 = {"file1_address": "file1_10000.txt"}
    response4 = client.post(url, data=json.dumps(json_input4))
    # assert response1.status_code == 500 and response1.get_data() == b'both file addresses are missing please enter file1_address and file2_address'
    assert response2.status_code == 500 and response2.get_data() == b'please enter file1_address and file2_address'
    assert response3.status_code == 500 and response3.get_data() == b'file1 address is missing'
    assert response4.status_code == 500 and response4.get_data() == b'file2 address is missing'


def test_file_path_exists():
    # to check both file address is not exist
    os.system("mkdir input")
    client = flask_code.application.test_client()
    url = '/file_compare/'
    json_input1 = {"file1_address": "file1_10.txt", "file2_address": "file2_10.txt"}
    response1 = client.post(url, data=json.dumps(json_input1))
    assert response1.status_code == 500 and response1.get_data() == b'Both files are not present'
    open("input/file2_10000.txt", 'w')
    json_input3 = {"file1_address": "file1_10.txt", "file2_address": "file2_10000.txt"}
    response3 = client.post(url, data=json.dumps(json_input3))
    assert response3.status_code == 500 and response3.get_data() == b'file1 is not present'
    open("input/file1_dummy.txt", 'w')
    json_input2 = {"file1_address": "file1_dummy.txt", "file2_address": "file2_dummy.txt"}
    response2 = client.post(url, data=json.dumps(json_input2))
    assert response2.status_code == 500 and response2.get_data() == b'file2 is not present'
    os.system("rm -rf input")


@pytest.mark.order(-1)
def test_token():  # race condition
    os.system("mkdir input")
    os.system("mkdir output")
    os.system("mkdir output/logs")
    os.system("mkdir output/number_of_lines")
    os.system("touch output/number_of_lines/number_of_lines.txt")
    open("input/file1.txt", 'w')
    open("input/file2.txt", 'w')
    client = flask_code.application.test_client()
    url = '/file_compare/'
    json_input1 = {"file1_address": "file1.txt", "file2_address": "file2.txt"}
    response3 = client.post(url, data=json.dumps(json_input1))
    assert response3.status_code == 200
    os.system("rm -rf output")
    os.system("rm -rf input")


def test_input_body_paginate():
    client = flask_code.application.test_client()
    url = '/paginate/'
    json_input1 = ''
    response1 = client.get(url, data=json_input1)
    assert response1.status_code == 500 and response1.get_data() == b'please enter the input body, body is empty'
    json_input2 = '{body is not in proper json format}'
    response2 = client.get(url, data=json_input2)
    assert response2.status_code == 500 and response2.get_data() == b'input not in proper format, input must be a json'


def test_key_missing():
    client = flask_code.application.test_client()
    url = '/paginate/'
    json_input2 = {"toke": "abcd", "page": 1}
    response2 = client.get(url, data=json.dumps(json_input2))
    assert response2.status_code == 500 and response2.get_data() == b'please enter token and page_number'
    json_input3 = {"page_number": 1}
    response3 = client.get(url, data=json.dumps(json_input3))
    assert response3.status_code == 500 and response3.get_data() == b'Please enter token'
    json_input4 = {"token": "abc"}
    response4 = client.get(url, data=json.dumps(json_input4))
    assert response4.status_code == 500 and response4.get_data() == b'Please enter the page number'


def test_invalid_input():
    client = flask_code.application.test_client()
    url = '/paginate/'
    json_input1 = {"token": "abc", "page_number": "a"}
    response1 = client.get(url, data=json.dumps(json_input1))
    assert response1.status_code == 500 and response1.get_data() == b'page number must be an integer'
    json_input2 = {"token": "invalid_toke", "page_number": 1}
    response2 = client.get(url, data=json.dumps(json_input2))
    assert response2.status_code == 500 and response2.get_data() == b'please enter the valid token'


def test_key_missing_file_compare():
    list1 = [{"id": "333l", "evt_order": 0, "user": "abc"},
             {"id": "334l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]
    output = file.sort_input_json(list1)
    assert output == -1


def test_expected_output():
    list1 = [{"id": 323, "raw_log_time": 10},
             {"id": 324, "raw_log_time": 11}]
    list2 = [{"id": 325, "raw_log_time": 12},
             {"id": 326, "raw_log_time": 13}]
    list3 = file.core_logic_json(list1, list2)
    assert list3 == ["{'id': 325, 'raw_log_time': 12}<mismatch>",
                     "{'id': 326, 'raw_log_time': 13}<mismatch>"]

    # check if sequence is repeating

    list1 = [{"id": 323, "raw_log_time": 10},  # Pune
             {"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 325, "raw_log_time": 12},  # Maharashtra
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 327, "raw_log_time": 14},  # Patna
             {"id": 323, "raw_log_time": 10},  # Pune
             {"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 325, "raw_log_time": 12},  # Maharrashtra
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 327, "raw_log_time": 14}  # Patna
             ]
    list2 = [{"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 328, "raw_log_time": 15},  # Kochi
             {"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 328, "raw_log_time": 15}]  # Kochi

    # as inputs are not sorted in term of raw_log_time so sorting need to be done
    sorted_list1 = file.sort_input_json(list1)
    sorted_list2 = file.sort_input_json(list2)

    list3 = file.core_logic_json(sorted_list1, sorted_list2)
    assert list3 == ['\n', '\n', {'id': 324, 'raw_log_time': 11}, {'id': 324, 'raw_log_time': 11}, '\n', '\n',
                     {'id': 326, 'raw_log_time': 13}, {'id': 326, 'raw_log_time': 13},
                     "{'id': 328, 'raw_log_time': 15}<mismatch>", "{'id': 328, 'raw_log_time': 15}<mismatch>"]

    list1 = [{"id": 323, "raw_log_time": 10},  # Pune
             {"id": 325, "raw_log_time": 12},  # Maharashrta
             {"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 323, "raw_log_time": 10},  # Pune
             {"id": 325, "raw_log_time": 12},  # Maharashrta
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 327, "raw_log_time": 14}  # Patna
             ]
    list2 = [{"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 328, "raw_log_time": 15},  # kochi
             {"id": 329, "raw_log_time": 16},  # kochi2
             {"id": 330, "raw_log_time": 17}  # kochi3
             ]
    sorted_list1 = file.sort_input_json(list1)
    sorted_list2 = file.sort_input_json(list2)
    list3 = file.core_logic_json(sorted_list1, sorted_list2)
    print(list3)

    list1 = [{"id": 323, "raw_log_time": 10},  # Pune
             {"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 325, "raw_log_time": 12},  # Maharashtra
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 327, "raw_log_time": 14},  # Patna
             {"id": 323, "raw_log_time": 10},  # Pune
             {"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 325, "raw_log_time": 12},  # Maharashtra
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 327, "raw_log_time": 14}  # Patna
             ]
    list2 = [{"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 328, "raw_log_time": 15},  # Kochi
             ]
    sorted_list1 = file.sort_input_json(list1)
    sorted_list2 = file.sort_input_json(list2)
    list3 = file.core_logic_json(sorted_list1, sorted_list2)
    assert list3 == ['\n', '\n', {'id': 324, 'raw_log_time': 11}, '\n', '\n', '\n', {'id': 326, 'raw_log_time': 13},
                     '\n', '\n', "{'id': 328, 'raw_log_time': 15}<mismatch>"]

    list1 = [{"id": 323, "raw_log_time": 10},  # Pune
             {"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 325, "raw_log_time": 12},  # Maharashtra
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 327, "raw_log_time": 14},  # Patna
             ]
    list2 = [{"id": 324, "raw_log_time": 11},  # Mumbai
             {"id": 326, "raw_log_time": 13},  # Delhi
             {"id": 328, "raw_log_time": 15},  # Kochi
             ]
    sorted_list1 = file.sort_input_json(list1)
    sorted_list2 = file.sort_input_json(list2)
    list3 = file.core_logic_json(sorted_list1, sorted_list2)
    assert list3 == ['\n', {'id': 324, 'raw_log_time': 11}, '\n', {'id': 326, 'raw_log_time': 13},
                     "{'id': 328, 'raw_log_time': 15}<mismatch>"]


def test_threading():
    file.total_threads = 3
    os.system("mkdir input")
    os.system("touch output/number_of_lines/number_of_lines.txt")
    open("input/file1.txt", 'w')
    open("input/file2.txt", 'w')
    client = flask_code.application.test_client()
    url = '/file_compare/'
    json_input1 = {"file1_address": "file1.txt", "file2_address": "file2.txt"}
    response1 = client.post(url, data=json.dumps(json_input1))
    assert response1.status_code == 500
    os.system("rm -rf output")
    file.total_threads = 0


def test_replace_single_quotes_with_double_quotes():
    os.system("mkdir input")
    with open("input/file1.txt", 'w') as f:
        f.write("{'id': 324, 'raw_log_time': 11}")

    file.replace_single_quotes_with_double_quotes("input/file1.txt")
    with open("input/file1.txt", "r") as f1:
        text = f1.read()
    assert text.count("'") == 0

    with open("input/file1.txt", 'w') as f:
        f.write("check for discard")

    file.replace_single_quotes_with_double_quotes("input/file1.txt")
    with open("input/file1.txt", "r") as f1:
        text = f1.read()
    assert text == ""
    os.system("rm -rf input")


def test_read_input_json():
    os.system("mkdir input")
    with open("input/file1.txt", 'w') as f:
        f.write("{'id': 324, 'raw_log_time': 11}")

    final_list = file.read_input_json("input/file1.txt")
    assert final_list == [{"id": 324, "raw_log_time": 11}]
    with open("input/file1.txt", 'w') as f:
        f.write("input not in json format")

    expected_result = file.read_input_json("input/file1.txt")
    assert expected_result == -1
    os.system("rm -rf input")


def test_read_input_text():
    os.system("mkdir input")
    with open("input/file1.txt", 'w') as f:
        f.write("B\n")
        f.write("A\n")
    sorted_list = file.read_input_text("input/file1.txt")
    # expect sorted list
    assert sorted_list == ["A", "B"]
    os.system("rm -rf input")


def test_sort_input_json():
    list1 = [{"id": 324, "raw_log_time": 11}, {"id": 324, "raw_log_time": 15}, {"id": 324, "raw_log_time": -11}]
    sorted_list = file.sort_input_json(list1)
    assert sorted_list == [{"id": 324, "raw_log_time": -11}, {"id": 324, "raw_log_time": 11},
                           {"id": 324, "raw_log_time": 15}]
    # check if raw_log_time present
    list1 = [{"id": 324, "raw_log_time": 11}, {"id": 324}, {"id": 324, "raw_log_time": -11}]
    expected_value_minus_one = file.sort_input_json(list1)
    assert expected_value_minus_one == -1


def test_main_functionality_for_json():
    os.system("mkdir input")
    with open("input/file1.txt", 'w') as f1:
        f1.write('{"id": 324, "raw_log_time": 1}\n')
        f1.write('{"id": 325, "raw_log_time": 111}\n')
        f1.write('{"id": 326, "raw_log_time": 11}\n')
        f1.write('{"id": 327, "raw_log_time": 5}\n')
        f1.write('{"id": 328, "raw_log_time": 4}\n')
        f1.write('{"id": 329, "raw_log_time": 15}\n')
        f1.write('{"id": 330, "raw_log_time": 18}\n')

    with open("input/file2.txt", 'w') as f2:
        f2.write('{"id": 324, "raw_log_time": 1}\n')
        f2.write('{"id": 325, "raw_log_time": 111}\n')
        f2.write('{"id": 326, "raw_log_time": 11}\n')
        f2.write('{"id": 327, "raw_log_time": 5}\n')
        f2.write('{"id": 328, "raw_log_time": 4}\n')
        f2.write('{"id": 329, "raw_log_time": 15}\n')
        f2.write('{"id": 330, "raw_log_time": 18}\n')

    code = "abc"
    is_json = file.main_code("input/file1.txt", "input/file2.txt", code)
    # above inputs contains json that's why we expect true
    assert is_json == True
    os.system("rm -rf input")


def test_main_functionality_for_text():
    os.system("mkdir input")
    with open("input/file3.txt", 'w') as f1:
        f1.write('input file contain text\n')
        f1.write('input file contain text2\n')
        f1.write('input file contain text3\n')
        f1.write('input file contain text4\n')
        f1.write('input file contain text5\n')
        f1.write('input file contain text6\n')
        f1.write('input file contain text7\n')

    with open("input/file4.txt", 'w') as f2:
        f2.write('input file contain text\n')
        f2.write('input file contain text2\n')
        f2.write('input file contain text3\n')
        f2.write('input file contain text4\n')
        f2.write('input file contain text5\n')
        f2.write('input file contain text6\n')
        f2.write('input file contain text7\n')

    is_json = file.main_code("input/file3.txt", "input/file4.txt", code="abc")
    # as above inputs contains only text so we expect false
    assert is_json == False
    os.system("rm -rf input")


def test_total_number_of_lines():
    os.system("mkdir output")
    os.system("mkdir output/number_of_lines")
    os.system("touch output/number_of_lines/number_of_lines.txt")
    list3 = ['{"id": 324, "raw_log_time": 1}'] * 200
    list3 = file.list_to_file(list3, code="testing_file")
    file.persist_file_length(list3, code="testing_file")
    client = flask_code.application.test_client()
    url = '/paginate/'
    json_input1 = {"token": "testing_file", "page_number": "0"}
    response1 = client.get(url, data=json.dumps(json_input1))
    assert response1.status_code == 200
    json_input1 = {"token": "testing_file", "page_number": "10"}
    response1 = client.get(url, data=json.dumps(json_input1))
    assert response1.status_code == 500 and response1.get_data() == b'total number of pages is 0'
    # now check what if output file is present but information of that file is not present in number_of_lines folder
    f = open("output/testing_file2.txt", "w")
    f.write('{"id": 324, "raw_log_time": 1}')
    f.close()
    client = flask_code.application.test_client()
    url = '/paginate/'
    json_input1 = {"token": "testing_file2", "page_number": "0"}
    response1 = client.get(url, data=json.dumps(json_input1))
    os.system("rm -rf output")
    assert response1.status_code == 500


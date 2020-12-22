from file_compare_both_inputs_sorted import main_func

def test_exact_same():
    list1 = [{"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"334l","raw_log_time":8,"evt_order":0,"user":"abc"}]

    list2 = [{"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"334l","raw_log_time":8,"evt_order":0,"user":"abc"}]

    list3 = main_func(list1, list2)
    assert list3 == [{'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '334l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}]


def test_exact_same_list1_greater():
    list1 = [{"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"334l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"335l","raw_log_time":8,"evt_order":0,"user":"abc"}]

    list2 = [{"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"334l","raw_log_time":8,"evt_order":0,"user":"abc"}]

    list3 = main_func(list1, list2)
    assert list3 == [{'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '334l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},'\n']


def test_exact_same_list2_greater():
    list1 = [{"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"334l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"335l","raw_log_time":8,"evt_order":0,"user":"abc"}]

    list2 = [{"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"334l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"335l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"336l","raw_log_time":8,"evt_order":0,"user":"abc"}]

    list3 = main_func(list1, list2)
    assert list3 == [{'id': '333l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '334l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     {'id': '335l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     "{'id': '336l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}<mismatch>"]


def test_differ():
    list1 = [{"id":"323l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"338l","raw_log_time":8,"evt_order":0,"user":"abc"}]

    list2 = [{"id":"323l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"338l","raw_log_time":8,"evt_order":0,"user":"abc"},
             {"id":"343l","raw_log_time":8,"evt_order":0,"user":"abc"}]

    list3 = main_func(list1, list2)
    assert list3 == [{'id': '323l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     '\n',
                     {'id': '338l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     "{'id': '343l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}<mismatch>"]


def test_differ_list1_greater():
    list1 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "338l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "344l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "346l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "348l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list2 = [{"id": "323l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "338l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "343l", "raw_log_time": 8, "evt_order": 0, "user": "abc"},
             {"id": "347l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}]

    list3 = main_func(list1, list2)

    assert list3 == [{'id': '323l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     '\n',
                     {'id': '338l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'},
                     "{'id': '343l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}<mismatch>",
                     '\n',
                     "{'id': '347l', 'raw_log_time': 8, 'evt_order': 0, 'user': 'abc'}<mismatch>",]



import fileCompareVennDiagram

def test_case1():
    list1 = ['Pune\n', 'Maharashtra\n', 'Mumbai\n', 'Delhi\n', 'Patna\n']
    list2 = ['Mumbai\n', 'Delhi\n', 'Kochi\n']
    list3 = fileCompareVennDiagram.func(list1, list2)
    assert list3 == ['\n', '\n', 'Mumbai\n', 'Delhi\n', 'Kochi<mismatch>\n']

def test_case2():
    list1 = ['Pune\n', 'Mumbai\n', 'Maharashtra\n', 'Delhi\n', 'Patna\n']
    list2 = ['Mumbai\n', 'Delhi\n', 'Kochi\n']
    list3 = fileCompareVennDiagram.func(list1, list2)
    assert list3 == ['\n', 'Mumbai\n','\n', 'Delhi\n', 'Kochi<mismatch>\n']

def test_case3():
    list1 = ['Pune\n', 'Mumbai\n', 'Maharashtra\n', 'Delhi\n', 'Patna\n', 'Pune\n', 'Mumbai\n', 'Maharashtra\n', 'Delhi\n', 'Patna\n']
    list2 = ['Mumbai\n', 'Delhi\n', 'Kochi\n', 'Mumbai\n', 'Delhi\n', 'Kochi\n']
    list3 = fileCompareVennDiagram.func(list1, list2)
    assert list3 == ['\n', 'Mumbai\n', '\n','Delhi\n', 'Kochi<mismatch>\n', '\n', 'Mumbai\n','\n', 'Delhi\n', 'Kochi<mismatch>\n']

def test_case4():
    list1 = ['Pune\n', 'Mumbai\n', 'Maharashtra\n', 'Delhi\n', 'Patna\n', 'Pune\n', 'Mumbai\n', 'Maharashtra\n', 'Delhi\n', 'Patna\n']
    list2 = ['Mumbai\n', 'Delhi\n', 'Kochi\n']
    list3 = fileCompareVennDiagram.func(list1, list2)
    assert list3 == ['\n', 'Mumbai\n', '\n', 'Delhi\n', '\n', '\n', '\n', '\n', '\n', 'Kochi<mismatch>\n']
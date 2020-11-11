import pytest
import file_compare

def test_case1():
    list1 = ['Pune\n', 'Maharashtra\n', 'Mumbai\n', 'Delhi\n', 'Patna\n']
    list2 = ['Mumbai\n', 'Delhi\n', 'Kochi\n']
    file_compare.func(list1,list2)
    list3 = file_compare.get_strings('./output.txt')
    assert list3 == ['\n', '\n', 'Mumbai\n', 'Delhi\n', 'Kochi <Mismatched>\n']

def test_case2():
    list1 = ['Pune\n', 'Mumbai\n', 'Maharashtra\n', 'Delhi\n', 'Patna\n']
    list2 = ['Mumbai\n', 'Delhi\n', 'Kochi\n']
    file_compare.func(list1,list2)
    list3 = file_compare.get_strings('./output.txt')
    assert list3 == ['\n', 'Mumbai\n', 'Delhi\n', 'Kochi <Mismatched>\n']

def test_case3():
    list1 = ['Pune\n', 'Mumbai\n', 'Maharashtra\n', 'Delhi\n', 'Patna\n', 'Pune\n', 'Mumbai\n', 'Maharashtra\n', 'Delhi\n', 'Patna\n']
    list2 = ['Mumbai\n', 'Delhi\n', 'Kochi\n', 'Mumbai\n', 'Delhi\n', 'Kochi\n']
    file_compare.func(list1,list2)
    list3 = file_compare.get_strings('./output.txt')
    assert list3 == ['\n', 'Mumbai\n', 'Delhi\n', 'Kochi <Mismatched>\n', '\n', 'Mumbai\n', 'Delhi\n', 'Kochi <Mismatched>\n']
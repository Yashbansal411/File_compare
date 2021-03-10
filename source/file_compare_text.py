import pandas as pd
import os
import json
from operator import itemgetter
import shutil


def read_input(file_address):
    df1 = pd.read_csv(file_address, sep='\n', header=None, iterator=True)
    input = df1.read()
    li = input.values.tolist()
    li = sorted(li, key=lambda l: l[0])
    for i in li:
        print(i)


read_input("file1_txt.txt")

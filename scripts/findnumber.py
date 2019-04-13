import os
import re
from utils.operateFiles import stripBracket


def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s

def str2int(v_str):
    return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]

def sort_humanly(v_list):
    return sorted(v_list, key=str2int)



dirPath = 'D:\Programming software\python\\file\django\mysite\media\\upload\X毛\X毛\少女映画-FGOX毛'
stripBracket(dirPath)
dirPath = dirPath.replace('\\','/')
print(sort_humanly(os.listdir(dirPath)))




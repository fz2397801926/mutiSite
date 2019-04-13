import os
import re
import zipfile
from mysite.settings import systemType

# 去除括号
def stripBracket(path):
    if systemType == 'WindowsPE':
        path = path.replace("\\", "/")
    print(path)
    for file in os.listdir(path):
        p1 = re.compile('[(](.*?)[)]')
        number = re.findall(p1, file)
        # print(number)
        if number != []:
            result = re.sub(p1, number[0], file)
            # print(result)
            # print(file)
            cwdPath = os.path.join(path, file)
            if systemType == 'WindowsPE':
                cwdPath = cwdPath.replace("\\", "/")
            print(cwdPath)
            cwdPathRe = os.path.join(path, result)
            if systemType == 'WindowsPE':
                cwdPathRe = cwdPathRe.replace("\\", "/")
            print(cwdPathRe)
            os.rename(cwdPath, cwdPathRe)
    return True

# 对文件名含数字的文件排序
def sortFile(fileList):
    def tryint(s):
        try:
            return int(s)
        except ValueError:
            return s

    def str2int(v_str):
        return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]

    return sorted(fileList, key=str2int)


# 解压zip
def unzipFile(filePath):
    zipFile = zipfile.ZipFile(filePath)
    if os.path.isdir(filePath + "Files"):
        pass
    else:
        os.mkdir(filePath + "Files")
    for names in zipFile.namelist():
        print(names)
        # zipFile.extract(names, filePath + "Files/")
    zipFile.close()

# 解压7z
def decom7zFile(filePath):
    if systemType == 'WindowsPE':
        command = '7z x ' + filePath
    else:
        command = '7za x ' + filePath
    print(command)
    try:
        status = os.system(command)
    except Exception:
        status = 'false'
    return status

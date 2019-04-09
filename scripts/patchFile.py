# 此脚本用于去除文件名中的括号
import os
import re
path = 'D:\software\下载\下载的文件\度娘的地盘\少女映画-玛修战斗服 111P\少女映画-玛修战斗服 111P'
path = path.replace("\\","/")
print(path)
for file in os.listdir(path):
    p1 = re.compile('[(](.*?)[)]')
    number = re.findall(p1,file)
    # print(number)
    if number != []:
        result = re.sub(p1,number[0],file)
        # print(result)
        # print(file)
        cwdPath = os.path.join(path,file)
        cwdPath = cwdPath.replace("\\","/")
        print(cwdPath)
        cwdPathRe = os.path.join(path,result)
        cwdPathRe = cwdPathRe.replace("\\", "/")
        print(cwdPathRe)
        os.rename(cwdPath,cwdPathRe)

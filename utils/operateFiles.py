import os
import zipfile
from mysite.settings import systemType
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

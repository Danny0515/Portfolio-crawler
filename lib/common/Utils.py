import json
import logging
import os


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(module)s-%(lineno)d [%(levelname)s] %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

def readJsonFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        jsonData = json.load(file)
    return jsonData

def writeJsonFile(filePath, jsonData):
    with open(filePath, 'w', encoding='utf-8') as file:
        file.write(json.dumps(jsonData, sort_keys=False, indent=4, separators=(',', ': ')))

def readLinesFromFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as f:
        return [line.replace('\n', '') for line in f.readlines()]

def readJsonStr(string):
    return json.loads(string)

def initJsonFile(path):
    if os.path.exists(path):
        return True
    else:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("{}")
        logging.info(f"Create new file or folder: {path}")
        return True

def createDirectory(path):
    if os.path.exists(path):
        return
    else:
        logging.info(f"Create new directory: {path}")
        os.mkdir(path)

def countIntervalsTime(startTime, finishTime):
    if startTime == 0:
        return 0
    return round(finishTime - startTime)

# 檢查 sourceDict 的 key 是否有在 checkTarget 裡
def checkIncludeKeys(sourceDict, checkTarget):
    checkResult = [key for key in sourceDict.keys() if key in checkTarget]
    if len(checkResult) != 0:
        return True
    else:
        return False


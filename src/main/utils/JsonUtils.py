import json
import os


class JsonUtils:
    @staticmethod
    def readJsonFile(filePath):
        with open(filePath, 'r', encoding='utf-8') as file:
            jsonData = json.load(file)
        return jsonData

    @staticmethod
    def writeJsonFile(filePath, jsonData):
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(jsonData, sort_keys=False, indent=4, separators=(',', ': ')))

    @staticmethod
    def readLinesFromFile(filePath) -> list:
        with open(filePath, 'r', encoding='utf-8') as f:
            return [line.replace('\n', '') for line in f.readlines()]
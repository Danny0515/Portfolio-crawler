class CrawlerUtils:
    @staticmethod
    def checkIncludeKeys(sourceDict, checkTarget):
        # 檢查 sourceDict 的 key 是否有在 checkTarget 裡
        checkResult = [key for key in sourceDict.keys() if key in checkTarget]
        if len(checkResult) != 0:
            return True
        else:
            return False

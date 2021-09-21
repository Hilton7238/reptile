class Movie:
    def __init__(self, cName, eName, score, img, url):
        self.__cName = cName
        self.__score = score
        self.__img = img
        self.__eName = eName
        self.__url = url

    def getcName(self):
        return self.__cName

    def getScore(self):
        return self.__score

    def getImg(self):
        return self.__img

    def getUrl(self):
        return self.__url

    def geteName(self):
        return self.__eName

    __url = ""
    __cName = ""
    __eName = ""
    __score = ""
    __img = ""

class Event:
    def __init__(self,date,subject):
        self.__date = date
        self.__subject = subject

    def getDate(self):
        return self.__date

    def setDate(self,date):
        self.__date = date
        
    def getSubject(self):
        return self.__subject
    
    def setSubject(self, subject):
        self.__subject = subject
import csv
from eventreader.event import Event
class EventReaderProcessor:
    
    def __init__(self, events_file_direcory="../events.csv"):
         self.__eventFileDirectory = events_file_direcory

    def process(self):
        """
        Read event from csv file

        :rtype: list[Event]
        :return: list of event
        """
        with open(self.__eventFileDirectory, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return [Event(row["date"], row["subject"]) for row in reader]

import dateparser
import datetime


class DateParser:
    def __init__(self, date_string):
        self.date_string = date_string

    def parse(self):
        if isinstance(self.date_string, datetime.datetime):
            return self.date_string
        try:
            return dateparser.parse(self.date_string)
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def dt_to_string(dt):
        return dt.strftime("%Y-%m-%d")

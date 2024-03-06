import json
import time


class BaseRequest:

    @staticmethod
    def timestamp_to_str(timestamp):
        formatted_time = time.strftime("%d %b %Y %H:%M:%S", time.localtime(timestamp))
        ms = int((timestamp % 1) * 1000)
        formatted_time = f"{formatted_time}.{ms:03d}"
        return formatted_time

    def to_json(self):
        return json.dumps(self.__dict__)


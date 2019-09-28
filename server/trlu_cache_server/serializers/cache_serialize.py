import json
import logging


class CacheJsonDecoder(json.JSONDecoder):
    def default(self, data):
        try:
            to_serialize = {
                'type': data.type,
                'data': {
                    'key': data.data.key,
                    'value': data.data.value,
                    'minutes': data.data.minutes
                }
            }
            return to_serialize
        except AttributeError:
            return super().default(data)


class CacheRespToClientJsonEncoder(json.JSONEncoder):
    def default(self, data):
        logging.debug(f"CacheRespToClientJsonEncoder, data type:")
        try:
            to_serialize = {
                'type': data['type'],
                'result': data['result'],
                'data': {
                    'key': data['data'].key,
                    'value': data['data'].value,
                    'date_stamp': data['data'].date_stamp,
                    'due_date': data['data'].due_date,
                    'state': data['data'].state
                }
            }
            return to_serialize
        except AttributeError:
            return super().default(data)


class CacheJsonEncoder(json.JSONEncoder):
    def default(self, data):
        try:
            to_serialize = {
                'type': data.value 
            }
            return to_serialize
        except AttributeError:
            return super().default(data)

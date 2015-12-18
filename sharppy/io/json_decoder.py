
import numpy as np

import sharppy.sharptab.profile as profile
import sharppy.sharptab.prof_collection as prof_collection
from decoder import Decoder

from datetime import datetime
from dateutil import parser
from json import loads

__fmtname__ = "json"
__classname__ = "JSONDecoder"

class JSONDecoder(Decoder):
    def __init__(self, file_name):
        super(JSONDecoder, self).__init__(file_name)

    def _parse(self):
        file_data = self._downloadFile()
        
        serialized_data = loads(file_data)
        
        for mem in serialized_data['profiles']:
            for prof in range(len(serialized_data['profiles'][mem])):
                serialized_data['profiles'][mem][prof]['date'] = parser.parse(serialized_data['profiles'][mem][prof]['date'])
                serialized_data['profiles'][mem][prof]['profile'] = 'raw'
                serialized_data['profiles'][mem][prof] = profile.create_profile(**serialized_data['profiles'][mem][prof])
        
        serialized_data['dates'] = [parser.parse(date) for date in serialized_data['dates']]
        
        prof_coll = prof_collection.ProfCollection(serialized_data['profiles'], serialized_data['dates'], **serialized_data['meta'])
        print(prof_coll)
        return prof_coll
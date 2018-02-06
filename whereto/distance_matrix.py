import json 
from urllib.parse import urlencode

from whereto import town_to_string

class DistanceMatrix:
  def __init__(self, api_key):
    self.api_key = api_key

  def url(self):
    origins = town_to_string(self.origin)
    destinations = '|'.join(
        [town_to_string(town) for town in self.destinations])
    return 'https://maps.googleapis.com/maps/api/distancematrix/json?' + \
           urlencode({
             'units': 'imperial',
             'origins': origins,
             'destinations': destinations,
             'key': self.api_key,
           })

  def apply_response(self, response):
    json_response = json.loads(response.decode('ascii'))
    self.destinations = [{**dest, 'distance': resp['distance'], 'duration': resp['duration']} for dest, resp in zip(self.destinations, json_response['rows'][0]['elements'])]

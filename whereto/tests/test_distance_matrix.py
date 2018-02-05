from unittest import TestCase

from whereto import DistanceMatrix

class TestDistanceMatrixUrl(TestCase):
  def setUp(self):
    self.maxDiff = None
    self.distance_matrix = DistanceMatrix('__MY_API_KEY__')
    self.distance_matrix.origin = {
      'commune': 'Calais',
      'department': 'Pas-de-Calais',
      'region': 'Nord-de-Pas-de-Calais',
    }

  def test_single_destination(self):
    self.distance_matrix.destinations = [{
      'commune': 'Paris',
      'department': 'Paris',
      'region': 'Ile-de-France',
    }]
    self.assertEqual('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Calais,Pas-de-Calais,Nord-de-Pas-de-Calais&destinations=Paris,Paris,Ile-de-France&key=__MY_API_KEY__',
                     self.distance_matrix.url())

  def test_multiple_destinations(self):
    self.distance_matrix.destinations = [{
      'commune': 'Paris',
      'department': 'Paris',
      'region': 'Ile-de-France',
    },{
      'commune': 'Bordeaux',
      'department': 'Gironde',
      'region': 'Aquitaine',
    }]
    self.assertEqual('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Calais,Pas-de-Calais,Nord-de-Pas-de-Calais&destinations=Paris,Paris,Ile-de-France|Bordeaux,Gironde,Aquitaine&key=__MY_API_KEY__',
                     self.distance_matrix.url())
                
class TestDistanceMatrixApplyResponse(TestDistanceMatrixUrl):
  def test_single_destination(self):
    self.distance_matrix.destinations = [{
      'commune': 'Paris',
      'department': 'Paris',
      'region': 'Ile-de-France',
    }]
    self.distance_matrix.apply_response(b'{\n   "destination_addresses" : [ "Paris, France" ],\n   "origin_addresses" : [ "Calais, France" ],\n   "rows" : [\n      {\n         "elements" : [\n            {\n               "distance" : {\n                  "text" : "182 mi",\n                  "value" : 292917\n               },\n               "duration" : {\n                  "text" : "3 hours 0 mins",\n                  "value" : 10827\n               },\n               "status" : "OK"\n            }\n         ]\n      }\n   ],\n   "status" : "OK"\n}\n')
    self.assertEqual([{
                        'commune': 'Paris',
                        'department': 'Paris',
                        'region': 'Ile-de-France',
                        'distance': {
                          'text': '182 mi',
                          'value': 292917,
                        },
                        'duration': {
                          'text': '3 hours 0 mins',
                          'value': 10827,
                        }
                      }],
                     self.distance_matrix.destinations)


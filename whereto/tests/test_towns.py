from unittest import TestCase

from whereto import parse_town, town_to_string

class TestParseTown(TestCase):
  def test_valid_row(self):
    self.assertEqual(
      {
        'rank': 4,
        'commune': 'Toulouse',
        'department': 'Haute-Garonne',
        'region': 'Midi-Pyrenees',
      },
      parse_town('4,Toulouse,Haute-Garonne,Midi-Pyrenees,"4,41,802"'))

class TestTownToString(TestCase):
  def test_valid_town(self):
    self.assertEqual('Toulouse,Haute-Garonne,Midi-Pyrenees',
                     town_to_string(
                      {
                        'rank': 4,
                        'commune': 'Toulouse',
                        'department': 'Haute-Garonne',
                        'region': 'Midi-Pyrenees',
                      }
                     )
                    )

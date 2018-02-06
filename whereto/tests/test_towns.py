from unittest import TestCase
from sqlite3 import Row

from whereto.town import parse, to_string, from_row

class TestParseTown(TestCase):
  def test_valid_row(self):
    self.assertEqual(
      {
        'rank': 4,
        'commune': 'Toulouse',
        'department': 'Haute-Garonne',
        'region': 'Midi-Pyrenees',
      },
      parse('4,Toulouse,Haute-Garonne,Midi-Pyrenees,"4,41,802"'))

class TestTownToString(TestCase):
  def test_valid_town(self):
    self.assertEqual('Toulouse,Haute-Garonne,Midi-Pyrenees',
                     to_string(
                      {
                        'rank': 4,
                        'commune': 'Toulouse',
                        'department': 'Haute-Garonne',
                        'region': 'Midi-Pyrenees',
                      }
                     )
                    )

class TestTownFromRow(TestCase):
  def test_all_fields(self):
    row = {
      'commune': 'c',
      'department': 'd',
      'region': 'r',
    }
    self.assertEqual({
                       'commune': 'c',
                       'department': 'd',
                       'region': 'r',
                     },from_row(row))

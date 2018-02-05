def parse_town(row):
  town = {}
  names = ['rank', 'commune', 'department', 'region']
  for name, value in zip(names, row.split(',')):
    town[name] = value
  try:
    town['rank'] = int(town['rank'])
  except ValueError:
    town = {}
  return town;
    
def load_towns(towns_csv):
  return [town for town in [parse_town(row) for row in towns_csv] if town]

def town_to_string(town):
  return '{},{},{}'.format(town['commune'],
                           town['department'],
                           town['region'])

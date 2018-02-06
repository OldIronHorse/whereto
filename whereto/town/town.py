def parse(row):
  town = {}
  names = ['rank', 'commune', 'department', 'region']
  for name, value in zip(names, row.split(',')):
    town[name] = value
  try:
    town['rank'] = int(town['rank'])
  except ValueError:
    town = {}
  return town;
    
def load(towns_csv):
  return [town for town in [parse(row) for row in towns_csv] if town]

def to_string(town):
  return '{},{},{}'.format(town['commune'],
                           town['department'],
                           town['region'])

def from_row(row):
  return {
    'commune': row['commune'],
    'department': row['department'],
    'region': row['region'],
  }

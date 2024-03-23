import json 

def ParseFile(parse_arg):
  with open(parse_arg['fname'], 'r') as data_file:
    result = {}
    # Parse header(first line)
    key_columns = data_file.readline().strip().split('\t')
    column_size = len(key_columns)
    if 'primary_key' in parse_arg:
      pk_index = key_columns.index(parse_arg['primary_key'])
    else:
      # Use line number as index, start from 1.
      pk_index = -1
    print('key columns size', column_size, ' pk is at', pk_index, key_columns)
    # Parse items.
    num_line = 0
    for line in data_file.readlines():
      if line.startswith('Expansion'): continue
      num_line += 1
      items = line.strip().split('\t')
      if len(items) != column_size:
        print('Item count does not match column_size', items)
        continue
      field_map = {}
      for i in range(len(items)):
        if items[i] and i != pk_index:
          field_map[key_columns[i]] = items[i]
      if pk_index >= 0:
        pk = items[pk_index]
      else:
        pk = str(num_line)
      result[pk] = field_map
  return result


if __name__ == '__main__':
  parse_arg = {
      'fname': 'MagicPrefix.txt',
  }
  result = {}
  magic_prefixes_pd2 = ParseFile(parse_arg)
  for k,v in magic_prefixes_pd2.items():
    result[k] = v['Name']
  print(result)
  open('magic_prefixes.json', 'w').write(
      json.dumps(result, indent=4))

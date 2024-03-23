import parse_file
import json 



if __name__ == '__main__':
  parse_arg = {
      'fname': 'ItemStatCost.txt',
      'primary_key': 'ID',
  }
  magic_attrs_pd2 = parse_file.ParseFile(parse_arg)
  magic_attrs = json.loads(open('../items_data/magic_attrs.json', 'r').read())
  merged_magic_attrs = {}
  conflict_magic_attrs = {}
  for pk, field_map in magic_attrs_pd2.items():
    bits = []
    bias = 0
    if 'Save Bits' in field_map:
      bits = [int(field_map['Save Bits'])]
    if 'Save Add' in field_map:
      bias = int(field_map['Save Add'])
    if pk in magic_attrs:
      if bits != magic_attrs[pk]['bits'] or bias != magic_attrs[pk]['bias']:
        conflict_magic_attrs[pk] = {
            'new': field_map,
            'old': magic_attrs[pk],
        }
      else:
        merged_magic_attrs[pk] = magic_attrs[pk]
        merged_magic_attrs[pk]['stat_name'] = field_map['Stat']
    else:
      conflict_magic_attrs[pk] = {
          'new': field_map
      }
  #json_object = json.dumps(ParseFile(parse_arg), indent = 4) 
  #print(json_object)
  open('merged_magic_attrs.json','w').write(json.dumps(merged_magic_attrs, indent = 4))
  open('conflict_magic_attrs.json','w').write(json.dumps(conflict_magic_attrs, indent = 4))
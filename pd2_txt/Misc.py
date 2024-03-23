import parse_file
import json 

if __name__ == '__main__':
  parse_arg = {
      'fname': 'Misc.txt',
      'primary_key': 'code',
  }
  result = {}
  misc_pd2 = parse_file.ParseFile(parse_arg)
  for k, v in misc_pd2.items():
    result[k] = v['*name']
  open('misc.json', 'w').write(
      json.dumps(result, indent=4))

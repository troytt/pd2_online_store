import parse_file
import json 

if __name__ == '__main__':
  parse_arg = {
      'fname': 'UniqueItems.txt',
  }
  result = {}
  misc_pd2 = parse_file.ParseFile(parse_arg)
  for k, v in misc_pd2.items():
    index = str(int(k) - 1)
    result[index] = v['index']
  open('unique.json', 'w').write(
      json.dumps(result, indent=4))

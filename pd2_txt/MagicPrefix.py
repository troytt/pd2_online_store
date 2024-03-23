import parse_file
import json 

def ParseMagic(input_name, output_name):
  parse_arg = {
      'fname': input_name,
  }
  result = {}
  magic_pd2 = parse_file.ParseFile(parse_arg)
  for k, v in magic_pd2.items():
    result[k] = v['Name']
  open(output_name, 'w').write(
      json.dumps(result, indent=4))
  

if __name__ == '__main__':
  ParseMagic('MagicPrefix.txt', 'magic_prefixes.json')
  ParseMagic('MagicSuffix.txt', 'magic_suffixes.json')

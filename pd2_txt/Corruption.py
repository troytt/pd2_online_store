import json 

result = {}

for line in open('Corruption.txt', 'r').readlines():
  items = line.strip().split('	', 1)
  if len(items) != 2:
    continue
  result[items[0]] = items[1]

open('corruption.json','w').write(json.dumps(result, indent = 4))

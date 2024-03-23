import parse_file
import json 
import re

def ParseMisc():
  parse_arg = {
      'fname': 'Misc.txt',
      'primary_key': 'code',
  }
  result = {}
  misc_pd2 = parse_file.ParseFile(parse_arg)
  for k, v in misc_pd2.items():
    sub_type = ''
    img_name = ''
    size = [1, 1]
    # amulet
    if k == 'amu':
      sub_type = 'amulet'
      img_name = 'amulet2.sprite.00.png'

    # body part

    # book
    if k == 'rtp' or k == 'tbk':
      sub_type = 'book'
      img_name = 'town_portal_book.sprite.00.png'
      size = [1, 2]
    if k == 'rid' or k == 'ibk':
      sub_type = 'book'
      img_name = 'identify_book.sprite.00.png'
      size = [1, 2]

    # charm
    if k == 'cm1' or k == 'cm2' or k == 'cm3':
      sub_type = 'charm'
      if k == 'cm1':
        img_name = 'charm_small.sprite.00.png'
      if k == 'cm2':
        img_name = 'charm_medium.sprite.00.png'
        size = [1, 2]
      if k == 'cm3':
        img_name = 'charm_large.sprite.00.png'
        size = [1, 3]
    # gem
    if k == 'jew' or k == 'jewf':
      sub_type = 'gem'
      img_name = 'perfect_diamond1.sprite.00.png'

    # gold

    # herb

    # key

    # map
    map_match = re.search(r"t\d\d", k)
    if map_match:
      sub_type = 'map'
      img_name = 'map.sprite.00.png'

    # potion

    # quest

    # quiver
    if k == 'aqv' or k == 'cqv':
        size = [1, 3]
        sub_type = 'quiver'
        if k == 'aqv':
            img_name = 'arrows.sprite.00.png'
        else:
            img_name = 'bolts.sprite.00.png'
    # ring
    if k == 'rin':
      sub_type = 'ring'
      img_name = 'ring.sprite.00.png'

    # rune
    rune_match = re.search(r"r\d\d", k)
    if rune_match:
      #print(rune_match.group())
      sub_type = 'rune'
      img_name = v['*name'].lower() + '_rune.sprite.00.png'

    result[k] = {
      'type': 'misc',
      'sub_type': sub_type,
      'img_name': img_name,
      'size_x': size[0],
      'size_y': size[1]
    }
  for code, r in result.items():
      print(code, r['type'], r['sub_type'], r['img_name'], r['size_x'], r['size_y'])
  
result = {}
parse_arg = {
    'fname': 'item_code_to_image.txt',
    'primary_key': 'code',
}
result = {}
misc_pd2 = parse_file.ParseFile(parse_arg)
for k, v in misc_pd2.items():
    result[k] = v
    result[k]['size_x'] = int(result[k]['size_x'])
    result[k]['size_y'] = int(result[k]['size_y'])
    print(k)
open('item_img.json', 'w').write(json.dumps(result, indent=4))

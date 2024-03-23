from classes import CLASS_NAMES
from errors import ItemParseError
from items_storage import ItemsDataStorage
from skills import SKILL_NAMES, ELE_SKILLS_NAMES, SKILLS_TREE_NAMES, SKILLS_TREE_OFFSETS
from utils import (
    ReverseBitReader,
    calc_bits_to_align,
    obj_to_dict,
    to_dict_list,
    print_binary_string,
)


class ItemDebug(object):
    """This class represents any item in the game."""

    _HEADER = 0x4D4A

    # Locations.
    LOC_STORED = 0x00
    LOC_EQUIPPED = 0x01
    LOC_BELT = 0x02
    LOC_CURSOR = 0x04
    LOC_SOCKETED = 0x06

    # Equipped locations.
    EQUIP_HEAD = 1
    EQUIP_NECK = 2
    EQUIP_TORSO = 3
    EQUIP_HAND_RIGHT = 4
    EQUIP_HAND_LEFT = 5
    EQUIP_FINGER_RIGHT = 6
    EQUIP_FINGER_LEFT = 7
    EQUIP_WAIST = 8
    EQUIP_FEET = 9
    EQUIP_HANDS = 10
    EQUIP_ALT_HAND_RIGHT = 11
    EQUIP_ALT_HAND_LEFT = 12

    # Panels.
    PANEL_NONE = 0
    PANEL_INVENTORY = 1
    PANEL_CUBE = 4
    PANEL_STASH = 5

    # Qualities (rarity).
    Q_LOW = 0x01
    Q_NORMAL = 0x02
    Q_HIGH = 0x03
    Q_MAGIC = 0x04
    Q_SET = 0x05
    Q_RARE = 0x06
    Q_UNIQUE = 0x07
    Q_CRAFTED = 0x08

    # Item types.
    T_ARMOR = 0
    T_SHIELD = 1
    T_WEAPON = 2
    T_MISC = 3

    _SET_EXTRA_COUNTS = {
        0: 0,
        1: 1,
        2: 1,
        3: 2,
        4: 1,
        6: 2,
        7: 3,
        10: 2,
        12: 2,
        15: 4,
        31: 5,
    }

    _items_data = ItemsDataStorage()

    def __init__(self, reader, debug=False):
        """Initializes an instance.

        :param reader: Byte stream.
        :type reader: io.BinaryIO
        """
        self._debug = debug
        # Simple
        self.is_identified = None
        self.is_socketed = None
        self.is_new = None
        self.is_ear = None
        self.is_start_item = None
        self.is_simple = None
        self.is_ethereal = None
        self.is_personalized = None
        self.is_runeword = None
        self.location_id = None
        self.equipped_id = None
        self.pos_x = None
        self.pos_y = None
        self.panel_id = None
        self.ear_char_class = None
        self.ear_char_level = None
        self.ear_char_name = None
        self.inserted_items_count = None
        self.version = None
        self.code = None

        # Advanced
        self.level = None
        self.has_multiple_pic = None
        self.is_class_specific = None
        self.pic_id = None
        self.personalized_name = None
        self.defense_rating = None
        self.max_durability = None
        self.cur_durability = None
        self.quantity = None
        self.socket_count = None
        self.magic_attrs = None
        self.set_extra_attrs = None
        self.set_req_items_count = None
        self.socketed_items = None
        self.iid = None
        self.rarity = None
        self.magic_prefix_id = None
        self.magic_suffix_id = None
        self.set_id = None
        self.rare_fname_id = None
        self.rare_sname_id = None
        self.rare_affixes = None
        self.unique_id = None
        self.runeword_id = None
        self.timestamp = None
        self.is_quantitative = None

        # Extra
        self.itype = None
        self.base_name = None
        self.is_magical = False
        self.is_rare = False
        self.is_set = False
        self.is_unique = False
        self.is_crafted = False

        self._reader = ReverseBitReader(reader)
        self._parse_simple()

        if not self.is_simple:
            self._parse_advanced()
        self._align_byte()
        print('full_name', self.name)

    def __str__(self):
        return f'{self.__class__.__name__}({self.code}: {self.name})'

    def __repr__(self):
        return self.__str__()

    @property
    def name(self):
        """Gets the special name for the item.

        If the item is not misc or simple then it has a special name otherwise
        only the base name.

        :return: Special name or base name
        :rtype: str
        """
        if self.is_magical:
            return self._items_data.get_magic_name(
                self.magic_prefix_id, self.magic_suffix_id
            )
        elif self.is_rare:
            return self._items_data.get_rare_name(
                self.rare_fname_id, self.rare_sname_id
            )
        elif self.is_set:
            return self._items_data.get_set_name(self.set_id)
        elif self.is_unique:
            return self._items_data.get_unique_name(self.unique_id)
        elif self.is_runeword:
            return self._items_data.get_runeword_name(self.runeword_id)
        return self.base_name

    def to_dict(self):
        """Dumps self to dictionary.

        :return: A dictionary with excluded private attributes such as _reader.
        :rtype: dict
        """
        item_dict = obj_to_dict(self, exclude=('_reader',))
        if self.socketed_items:
            item_dict['socketed_items'] = to_dict_list(self.socketed_items)
        item_dict['name'] = self.name
        return item_dict

    def _align_byte(self):
        """Align stream by byte boundary.

        :return: None
        """
        self._reader.read(calc_bits_to_align(self._reader.bits_total))

    def _parse_simple(self):
        """Parses attributes that have all items.

        :raises ItemParseError:
        :return: None
        """
        print('=======parse_simple=======')
        header_id = self._reader.read(16)
        if header_id != self._HEADER:
            raise ItemParseError(f'Invalid item header id: {header_id:02X}')
        print('header_id', header_id)
        self._reader.read(4)
        self.is_identified = bool(self._reader.read(1))
        print('is_identified', self.is_identified)
        self._reader.read(6)
        self.is_socketed = bool(self._reader.read(1))
        print('is_socketed', self.is_socketed)
        self._reader.read(1)
        # is_new - picked up since the last time the game was saved.
        self.is_new = bool(self._reader.read(1))
        print('is_new', self.is_new)
        self._reader.read(2)
        self.is_ear = bool(self._reader.read(1))
        print('is_ear', self.is_ear)
        self.is_start_item = bool(self._reader.read(1))
        print('is_start_item', self.is_start_item)
        self._reader.read(3)
        # is_simple - only contains 111 bits of data.
        self.is_simple = bool(self._reader.read(1))
        print('is_simple', self.is_simple)
        self.is_ethereal = bool(self._reader.read(1))
        print('is_ethereal', self.is_ethereal)
        self._reader.read(1)
        self.is_personalized = bool(self._reader.read(1))
        print('is_personalized', self.is_personalized)
        self._reader.read(1)
        self.is_runeword = bool(self._reader.read(1))
        print('is_runeword', self.is_runeword)
        self._reader.read(5)
        self.version = self._reader.read(8)
        print('version', self.version)
        self._reader.read(2)
        self.location_id = self._reader.read(3)
        print('location_id', self.location_id)
        self.equipped_id = self._reader.read(4)
        print('equipped_id', self.equipped_id)
        self.pos_x = self._reader.read(4)
        print('pos_x', self.pos_x)
        self.pos_y = self._reader.read(4)
        print('pos_y', self.pos_y)
        #self._reader.read(1)
        self.panel_id = self._reader.read(3)
        print('panel_id', self.panel_id)

        if self.is_ear:
            self.code = 'ear'
            self.base_name = self._items_data.get_misc_name(self.code)
            self.ear_char_class = CLASS_NAMES.get(self._reader.read(3))
            self.ear_char_level = self._reader.read(7)
            self.ear_char_name = self._reader.read_null_term_bstr(7).decode()
            print('ear: name: ', self.ear_char_name)
        else:
            self.code = ''.join(
                chr(self._reader.read(8)) for _ in range(4)
            ).rstrip()
            print('code', self.code)
            if self._items_data.is_armor(self.code):
                self.itype = self.T_ARMOR
                self.base_name = self._items_data.get_armor_name(self.code)
            elif self._items_data.is_shield(self.code):
                self.itype = self.T_SHIELD
                self.base_name = self._items_data.get_shield_name(self.code)
            elif self._items_data.is_weapon(self.code):
                self.itype = self.T_WEAPON
                self.base_name = self._items_data.get_weapon_name(self.code)
            else:
                self.itype = self.T_MISC
                self.base_name = self._items_data.get_misc_name(self.code)
            print('item_type', self.itype, 'base_name', self.base_name)

            self.is_quantitative = self._items_data.is_quantitative(self.code)
            print('is_quantitative', self.is_quantitative)
            self.inserted_items_count = self._reader.read(3)
            print('inserted_items_count', self.inserted_items_count)

            if self.inserted_items_count > 0:
                print('inserted_items_count', self.inserted_items_count)
                self.socketed_items = []
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    def _parse_magic_attrs(self):
        """Parses magic attributes.

        If the attribute does not make sense, then it is ignored, for example:
        the visual effect.

        :raises ItemParseError:
        :return: A list of string
        :rtype: list
        """
        print('=========parse_magic_attrs=========')
        magic_attrs_list = []
        attr_count = 0
        while True:
            attr_count += 1
            print('parse attr no: ', attr_count)
            magic_attr_id = self._reader.read(9)
            if magic_attr_id == 0x1FF:
                break
            print('magic_attr_id', magic_attr_id)
            attr_dict = self._items_data.get_magic_attr(magic_attr_id)
            if not attr_dict:
                raise ItemParseError(
                    f'Unknown magic attribute id: {magic_attr_id}'
                )
            bias = attr_dict.get('bias', 0)
            values = [
                self._reader.read(bits) - bias for bits in attr_dict['bits']
            ]
            print('values', values)

            if attr_dict.get('is_invisible', False):
                continue
            print('is_invisible', attr_dict['is_invisible'])

            if magic_attr_id in (83, 84):
                values[0] = CLASS_NAMES.get(values[0])
            elif magic_attr_id in (97, 107, 151, 204, 359):
                values[1] = SKILL_NAMES.get(values[1])
            elif magic_attr_id == 188:
                values[0] = SKILLS_TREE_NAMES.get(values[0])
                values[1] = CLASS_NAMES.get(values[1])
            elif magic_attr_id in range(195, 202):
                values[1] = SKILL_NAMES.get(values[1])
            elif magic_attr_id == 126:
                values[0] = ELE_SKILLS_NAMES.get(values[0])
            elif magic_attr_id == 360:
                values[1] = self._items_data.get_corruption(values[1])
            # 214-250 - based on char level (value * 0.125)% per level).
            magic_attrs_list.append(attr_dict['name'].format(*values))
            print('full_attr_str:', attr_dict['name'].format(*values))
            print('---')
            if len(magic_attrs_list) > 20:
                break
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        return magic_attrs_list

    def _parse_advanced(self):
        """Parses advanced attributes.

        If item is not simple, then it has additional attributes.

        :return: None
        """
        print('=======parse_advance=======')

        self.iid = self._reader.read(32)
        print('iid', self.iid)
        self.level = self._reader.read(7)
        print('level', self.level)
        self.rarity = self._reader.read(4)
        print('rarity', self.rarity)

        if self.rarity == self.Q_MAGIC:
            self.is_magical = True
            print('Q_MAGIC')
        elif self.rarity == self.Q_RARE:
            self.is_rare = True
            print('Q_RARE')
        elif self.rarity == self.Q_SET:
            self.is_set = True
            print('Q_SET')
        elif self.rarity == self.Q_UNIQUE:
            self.is_unique = True
            print('Q_UNIQUE')
        elif self.rarity == self.Q_CRAFTED:
            self.is_crafted = True
            print('Q_CRAFTED')

        self.has_multiple_pic = bool(self._reader.read(1))
        if self.has_multiple_pic:
            self.pic_id = self._reader.read(3)
            print('pic_id', self.pic_id)

        self.is_class_specific = bool(self._reader.read(1))
        print('is_class_specific', self.is_class_specific)
        if self.is_class_specific:
            self._reader.read(11)

        if self.rarity in (self.Q_LOW, self.Q_HIGH):
            self._reader.read(3)
        elif self.is_magical:
            self.magic_prefix_id = self._reader.read(11)
            self.magic_suffix_id = self._reader.read(11)
            print('magic_prefix_id', self.magic_prefix_id)
            print('magic_suffix_id', self.magic_suffix_id)
        elif self.is_set:
            self.set_id = self._reader.read(12)
            print('set_id', self.set_id)
        elif self.is_rare or self.is_crafted:
            self.rare_fname_id = self._reader.read(8)
            self.rare_sname_id = self._reader.read(8)
            print('rare_fname_id', self.rare_fname_id)
            print('rare_sname_id', self.rare_sname_id)
            self.rare_affixes = []
            for _ in range(6):
                if self._reader.read(1):
                    self.rare_affixes.append(self._reader.read(11))
            print('rare_affixes', self.rare_affixes)
        elif self.is_unique:
            self.unique_id = self._reader.read(12)
            print('unique_id', self.unique_id)

        if self.is_runeword:
            self.runeword_id = self._reader.read(12)
            print('runeword_id', self.runeword_id)
            self._reader.read(4)

        if self.is_personalized:
            self.personalized_name = self._reader.read_null_term_bstr(7)
            print('personalized_name', self.personalized_name)

        # Item is the Tome of portal/identify.
        if self.code in ('tbk', 'ibk'):
            self._reader.read(5)

        self.timestamp = self._reader.read(1)
        print('timestamp', self.timestamp)

        if self.itype in (self.T_ARMOR, self.T_SHIELD):
            self.defense_rating = self._reader.read(11) - 10
            print('defense_rating', self.defense_rating)
        if self.itype in (self.T_ARMOR, self.T_SHIELD, self.T_WEAPON):
            self.max_durability = self._reader.read(8)
            if self.max_durability > 0:
                self.cur_durability = self._reader.read(8)
                print('max_durability', self.max_durability, 'cur_durability', self.cur_durability)
                self._reader.read(1)

        if self.is_quantitative:
            self.quantity = self._reader.read(9)
            print('quantity', self.quantity)

        if self.is_socketed:
            self.socket_count = self._reader.read(4)
            print('socket_count', self.socket_count)

        extra_set_id = None
        set_extra_count = None

        if self.is_set:
            extra_set_id = self._reader.read(5)
            print('extra_set_id', extra_set_id)
            set_extra_count = self._SET_EXTRA_COUNTS.get(extra_set_id)
            print('set_extra_count', set_extra_count)

        self.magic_attrs = self._parse_magic_attrs()

        if set_extra_count:
            self.set_extra_attrs = []
            for _ in range(set_extra_count):
                self.set_extra_attrs.append(self._parse_magic_attrs()[0])

            # Item is not the Civerb's Ward.
            if self.set_id != 0:
                self.set_req_items_count = []
                for offset in range(5):
                    if (extra_set_id & (1 << offset)) == 0:
                        continue
                    self.set_req_items_count.append(offset + 2)

        if self.is_runeword:
            self.magic_attrs.extend(self._parse_magic_attrs())
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

if __name__ == '__main__':
    stop = 0
    for i in range(0, 1000):
        reader = open('test/item/item%d.d2i' % i, 'rb')
        print('test/item/item%d.d2i' % i)
        item = ItemDebug(reader)
        #try:
        #    item = ItemDebug(reader)
        #except:
        #    pass
        if i > stop:
            input()
# https://wiki.projectdiablo2.com/wiki/Item_Filtering#Armor
# https://github.com/BetweenWalls/PD2-Singleplayer/tree/main/Diablo%20II/ProjectD2/data/global/excel/modpacks/official
# https://squeek502.github.io/d2itemreader/formats/d2.html#item-data-format
# https://hexed.it/

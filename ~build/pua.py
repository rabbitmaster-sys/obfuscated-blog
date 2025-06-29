from fontTools.ttLib import TTFont
import random
import json

char_pua_map = {}
puas = [chr(code_point) for code_point in range(0xE000, 0xF900)]
char_set = [
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
  'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
  'U', 'V', 'W', 'X', 'Y', 'Z',
  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
  'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
  'u', 'v', 'w', 'x', 'y', 'z',
  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
  ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')',
  '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
  '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{',
  '|', '}', '~'
]

def randomPua():
    rand = random.choice(puas)
    puas.remove(rand)
    return ord(rand);

def main():
    font_path = "~build/payload.ttf"
    out_path = "assets/fonts/main.ttf"

    font = TTFont(font_path)

    # removing metas
    name_table = font['name']
    for record in name_table.names:
        if record.nameID in [1, 2, 3, 4, 6]: continue; # pass all main meta's
        record.string = b''

    old_glyph_order = font.getGlyphOrder()
    print(old_glyph_order)
    # TODO randomize glyphs
    new_glyph_order = [f"glyph{i:04d}" for i in range(len(old_glyph_order))]
    glyph_rename_map = dict(zip(old_glyph_order,new_glyph_order))

    cmap_table = None
    for table in font['cmap'].tables:
        if table.isUnicode():
            cmap_table = table
            break

    if not cmap_table:
        raise RuntimeError("Cmap Errr")

    new_cmap = {}
    for d, char in enumerate(char_set):
        original_code = ord(char)
        pua_code = randomPua();

        glyph_name = cmap_table.cmap.get(original_code)
        if not glyph_name:
            print(f"Warning:'{char}' (U+{original_code}) not found -> Skipping")
            continue

        new_name = glyph_rename_map.get(glyph_name)
        if original_code in cmap_table.cmap:
            del cmap_table.cmap[original_code]

        cmap_table.cmap[pua_code] = new_name
        print("Check: Is accessible by `char`=> ",cmap_table.cmap.get(original_code))
        char_pua_map[char] = pua_code
        print(f"Info: {glyph_name} is '{new_name}'")

    # TODO Remove unused char or maybe not (unoptimized/non-viable)
    for code in list(cmap_table.cmap.keys()):
        if code not in char_pua_map.values():
            del cmap_table.cmap[code]

    # Remove other attack vectors.
    # postsrpt
    if 'post' in font:
        font['post'].formatType = 3.0
        font['post'].extraNames = []
        font['post'].mapping = {}

    # gsub and gpos
    for table in ['GSUB', 'GPOS']:
        if table in font:
            del font[table]
    
    # head-meta(not-needed-ig)
    if 'head' in font:
        font['head'].created = 0
        font['head'].modified = 0
    
    if 'OS/2' in font:
        font['OS/2'].achVendID = '    '

    font.setGlyphOrder(new_glyph_order)
    font.save(out_path)
    with open("_plugins/map.json","w") as f:
        json.dump(char_pua_map,f);

    print(f"Info: Saved {out_path}")

if __name__ == "__main__":
    main()

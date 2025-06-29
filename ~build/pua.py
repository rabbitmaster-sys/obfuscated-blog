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
    font_path = "/workspaces/obfuscated-blog/~build/payload.ttf"
    out_path = "/workspaces/obfuscated-blog/assets/fonts/main.ttf"

    font = TTFont(font_path)

    cmap_table = None
    for table in font['cmap'].tables:
        if table.isUnicode():
            cmap_table = table
            break

    if not cmap_table:
        raise RuntimeError("Cmap Errr")

    for d, char in enumerate(char_set):
        original_code = ord(char)
        pua_code = randomPua();

        glyph_name = cmap_table.cmap.get(original_code)
        if not glyph_name:
            print(f"Warning:'{char}' (U+{original_code}) not found -> Skipping")
            continue

        if original_code in cmap_table.cmap:
            del cmap_table.cmap[original_code]

        cmap_table.cmap[pua_code] = glyph_name
        char_pua_map[char] = pua_code
        print(f"Info: U+{pua_code} to glyph '{glyph_name}'")

    font.save(out_path)
    with open("/workspaces/obfuscated-blog/_plugins/map.json","w") as f:
        json.dump(char_pua_map,f);

    print(f"Info: Saved {out_path}")

if __name__ == "__main__":
    main()

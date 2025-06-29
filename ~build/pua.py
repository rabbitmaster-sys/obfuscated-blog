from fontTools.ttLib import TTFont

# Your chars to remap
chars_to_map = (
    [chr(c) for c in range(ord('A'), ord('Z') + 1)] +
    [chr(c) for c in range(ord('a'), ord('z') + 1)] +
    [chr(c) for c in range(ord('0'), ord('9') + 1)] +
    [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
     ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
)

start_code = 0xE001  # PUA start

def main():
    font_path = "/workspaces/obfuscated-blog/~build/payload.ttf"
    out_path = "/workspaces/obfuscated-blog/assets/fonts/main.ttf"

    font = TTFont(font_path)

    # Find Unicode cmap subtable to modify
    cmap_table = None
    for table in font['cmap'].tables:
        if table.isUnicode():
            cmap_table = table
            break

    if not cmap_table:
        raise RuntimeError("No Unicode cmap subtable found")

    # For each char, map PUA codepoint to the glyph of the char
    for idx, char in enumerate(chars_to_map):
        original_code = ord(char)
        pua_code = start_code + idx

        glyph_name = cmap_table.cmap.get(original_code)
        if not glyph_name:
            print(f"Warning: Glyph for '{char}' (U+{original_code:04X}) not found in font")
            continue

        # Add or overwrite cmap entry for PUA codepoint
        cmap_table.cmap[pua_code] = glyph_name
        print(f"Mapped U+{pua_code:04X} to glyph '{glyph_name}' for char '{char}'")

    # Save new font
    font.save(out_path)
    print(f"Saved modified font to {out_path}")

if __name__ == "__main__":
    main()

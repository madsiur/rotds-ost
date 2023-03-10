import os, shutil, sys
from mass_extract import mass_extract
from monsters import create_monster_json
import constants as c
import json

def generate_json(roms, brrs, js_dir):
    dirs = []
    for k1, v1 in roms.items():
        entries = []
        dirs.append(k1)
        for k2, v2 in v1.items():
            entry = {
                "id": k2,
                "filename": v2[0],
                "title": v2[1],
                "game": v2[2],
                "composer": v2[3],
                "arranger": v2[4],
                "duration": v2[5],
            }
            entries.append(entry)
        json_object = json.dumps(entries, indent=4)
        file_string = f'const {k1} = \n{json_object};'

        this_fn = os.path.join(js_dir, f"{k1}.js")
        try:
            with open(this_fn, "w") as f:
                f.write(file_string)
        except IOError:
            print("ERROR: failed to write {this_fn}")
            sys.exit()

    json_object = json.dumps(dirs, indent=4)
    file_string = f'const dirs = \n{json_object};'
    this_fn = os.path.join(js_dir, "common.js")
    try:
        with open(this_fn, "w") as f:
            f.write(file_string)
    except IOError:
        print("ERROR: failed to write {this_fn}")
        sys.exit()

    entries = []
    for k, v in brrs.items():
        entry = {
            "id": k,
            "name": v[0],
            "gameShort": v[1],
            "gameLong": v[2],
            "loop": v[3],
            "env": v[4],
            "pitch": v[5],
            "size": v[6],
            "occ": v[7],
            "filename": v[8],
        }
        entries.append(entry)

    json_object = json.dumps(entries, indent=4)
    file_string = f'const brrs = \n{json_object};'

    this_fn = os.path.join(js_dir, "brrs.js")
    try:
        with open(this_fn, "w") as f:
            f.write(file_string)
    except IOError:
        print("ERROR: failed to write {this_fn}")
        sys.exit()

if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    common_dir = os.path.join(parent_dir, c.COMMON_DIR)
    js_dir = os.path.join(parent_dir, c.WEBSITE_DIR, "js", "generated")

    #rom, roms, brrs = mass_extract('mass_extract.txt')
    #generate_json(roms, brrs, js_dir)

    try:
        with open("ost_a.smc", 'rb') as f:
            rom = f.read()
    except IOError:
        print(f"ERROR: Couldn't load ROM file")
        sys.exit()
    if len(rom) % 0x10000 == 0x200:
        rom = rom[0x200:]
        print(f"Loaded rom with header for monsters.")
    else:
        print(f"Loaded rom without header for monsters.")

    if os.path.exists(common_dir):
        shutil.rmtree(common_dir)
    os.makedirs(common_dir)

    json_object = create_monster_json(rom)

    this_fn = os.path.join(common_dir, "monsters.json")
    try:
        with open(this_fn, "w") as f:
            f.write(json_object)
    except IOError:
        print("ERROR: failed to write {this_fn}")
        sys.exit()
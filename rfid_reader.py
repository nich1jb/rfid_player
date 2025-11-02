
#!/usr/bin/env python3
import vlc

MUSIC_FILE = "/mnt/nas/media/music/No Surprises.mp3"
player = vlc.MediaPlayer()

import sys

HID_KEYCODES = {
    0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4',
    0x22: '5', 0x23: '6', 0x24: '7', 0x25: '8',
    0x26: '9', 0x27: '0',
    0x28: '\n'  # Enter
}

with open('/dev/hidraw0', 'rb') as f:
    code = ''
    while True:
        data = f.read(16)
        key = data[2]
        if key == 0:
            continue
        if key == 0x28:  # Enter means end of tag
            print("Tag scanned:", code)
            code = ''
        else:
            code += HID_KEYCODES.get(key, '')

# device = "/dev/hidraw0"  # change if needed
# with open(device, "rb") as f:
#     print(f"Listening on {device}... (Ctrl+C to quit)")
#     while True:
#         data = f.read(16)
#         print(data)

# while True:
# 	tag_id, _ = reader.read()
# 	print(tag_id)
# 	if str(tag_id) in tag_map:
# 		player.set_mrl(tag_map[str(tag_id)])
# 		player.play()

# while True:
# 	cmd = input("(p)lay, (s)top, (q)uit: ").strip().lower()
# 	if cmd == "p":
# 		player.play()
# 		print("No playing 'No Surprises - Radiohead'")
# 	elif cmd == "s":
# 		player.stop()
# 	elif cmd == "q":
# 		player.stop()
# 		break

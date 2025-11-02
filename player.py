
#!/usr/bin/env python3
import vlc
from mfrc522 import MFRC522

MUSIC_FILE = "/mnt/nas/media/music/No Surprises.mp3"
player = vlc.MediaPlayer()
reader = MFRC522()
tag_map = {"123456": MUSIC_FILE}

status =  None
while status != reader.MI_OK:
	(status, TagType) = reader.Request(reader.PICC_REQIDL)
	if status == reader.MI_OK:
		print("Connection Success!")

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

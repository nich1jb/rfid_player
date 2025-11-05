
#!/usr/bin/env python3
import vlc
import time
from evdev import InputDevice, categorize, ecodes

NO_SURPRISES = "/mnt/nas/media/music/music_box/Radiohead/No Surprises.mp3"
KARMA_POLICE = "/mnt/nas/media/music/music_box/Radiohead/Karma Police.mp3"
DEVICE_PATH = '/dev/input/event4'
SONG_LIST = [
    NO_SURPRISES,
    KARMA_POLICE
]
instance = vlc.Instance()
player = instance.media_player_new()

current_index = 0

def play_song(index):
    media = instance.media_new(SONG_LIST[index])
    player.set_media(media)
    player.play()
    print(f"Now playing: {SONG_LIST[index]}")

# --- MAIN LOOP ---
device = InputDevice(DEVICE_PATH)
print(f"Listening for events from {device.name}")

play_song(current_index)

for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)

        if key_event.keycode == 'KEY_PLAYPAUSE' and key_event.keystate == key_event.key_down:
            state = player.get_state()
            if state == vlc.State.Playing:
                player.pause()
            elif state == vlc.State.Paused:
                player.play()

        if key_event.keycode == 'KEY_NEXTSONG' and key_event.keystate == key_event.key_down:
            current_index = (current_index + 1) % len(SONG_LIST)
            play_song(current_index)

        if key_event.keycode == 'KEY_PREVIOUSSONG' and key_event.keystate == key_event.key_down:
            if player.get_time() < 2000 and current_index > 0:
                current_index = (current_index - 1) % len(SONG_LIST)
                play_song(current_index)
            else:
                player.set_time(0)

    # Optional: check if song finished automatically
    if player.get_state() not in {1, 2, 3, 4}:  # playing/paused states
        current_index = (current_index + 1) % len(SONG_LIST)
        play_song(current_index)
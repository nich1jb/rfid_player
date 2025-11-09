#!/usr/bin/env python3
import vlc
import time
import os
from evdev import InputDevice, categorize, ecodes
import sys
import json

DEVICE_PATH = '/dev/input/event4'

MUSIC_FOLDER_NOT_FOUND = "/mnt/nas/media/music/music_box/TEST/"

instance = vlc.Instance("--file-caching=5000")
player = instance.media_player_new()
event_manager = player.event_manager()

current_index = 0
song_finished = False

with open("tag_mappings.json", "r") as f:
    tag_mappings = json.load(f)

if len(sys.argv) > 1:
    tag_uid = sys.argv[1]
    print("Tag UID:", tag_uid)
    if tag_uid in tag_mappings:
        music_folder = tag_mappings[tag_uid]["folder"]
    else:
        print("Tag UID not found")
        music_folder = MUSIC_FOLDER_NOT_FOUND

def create_song_list(folder):
    return [
        os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if f.lower().endswith(".mp3")
    ]

SONG_LIST = create_song_list(music_folder)


def play_song(index):
    global song_finished
    song_finished = False
    media = instance.media_new(SONG_LIST[index])
    player.set_media(media)
    player.play()
    print(f"Now playing: {SONG_LIST[index]}")


def on_song_end(event):
    global song_finished
    song_finished = True


def next_song():
    global current_index
    current_index = (current_index + 1) % len(SONG_LIST)
    play_song(current_index)


def previous_song():
    global current_index
    if player.get_time() < 2000 and current_index > 0:
        current_index = (current_index - 1) % len(SONG_LIST)
        play_song(current_index)
    else:
        player.set_time(0)


def main():
    global current_index, song_finished

    event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, on_song_end)

    device = InputDevice(DEVICE_PATH)
    play_song(current_index)

    while True:
        r, w, x = select.select([device.fd], [], [], 0.1)  # non-blocking
        if r:
            for event in device.read():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)

                    if key_event.keycode == 'KEY_PLAYPAUSE' and key_event.keystate == key_event.key_down:
                        state = player.get_state()
                        if state == vlc.State.Playing:
                            player.pause()
                        elif state == vlc.State.Paused:
                            player.play()

                    elif key_event.keycode == 'KEY_NEXTSONG' and key_event.keystate == key_event.key_down:
                        next_song()

                    elif key_event.keycode == 'KEY_PREVIOUSSONG' and key_event.keystate == key_event.key_down:
                        previous_song()

        if song_finished:
            song_finished = False
            next_song()

        time.sleep(0.1)


if __name__ == "__main__":
    import select
    main()

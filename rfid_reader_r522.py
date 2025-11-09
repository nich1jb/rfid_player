from mfrc522 import MFRC522
import RPi.GPIO as GPIO
import time
import subprocess
import threading

TAG_TIMEOUT = 1.0

def start_player(tag_uid):
  global player_process
  print("🎵 Starting player.py")
  player_process = subprocess.Popen(["python3", "player.py", str(tag_uid)])

def stop_player():
  global player_process
  if player_process and player_process.poll() is None:
    print("🛑 Stopping player.py")
    player_process.terminate()
    player_process.wait()
    player_process = None

def main():
  reader = MFRC522()
  tag_detected = False
  tag_thread = None
  stop_thread = threading.Event()
  last_seen = 0
  print("Scan a tag...")
  
  try:
    while True:
      (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

      if status == reader.MI_OK:
        last_seen = time.time()
        if not tag_detected:
          tag_detected = True
          print("Tag detected")
          (status, uid) = reader.MFRC522_Anticoll()
          if status == reader.MI_OK:
            tag_uid = "".join([str(x) for x in uid])
            start_player(tag_uid)

      elif tag_detected and (time.time() - last_seen > TAG_TIMEOUT):
        tag_detected = False
        print("Tag removed")
        stop_player()

      time.sleep(0.1)
  finally:
    GPIO.cleanup()
    stop_player()

if __name__ == "__main__":
  main()
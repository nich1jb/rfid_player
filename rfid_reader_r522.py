from mfrc522 import MFRC522
import RPi.GPIO as GPIO
import time

reader = MFRC522()

print("Scan a tag...")

try:
  while True:
    (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
    if status == reader.MI_OK:
      print("Tag detected")
      (status, uid) = reader.MFRC522_Anticoll()
      if status == reader.MI_OK:
        print("Card UID:", uid)
        print("Full UID:", "".join([str(x) for x in uid]))
        time.sleep(2)  # prevent multiple reads per second
    # else:
    #   status = reader.MFRC522_Request(reader.PICC_REQIDL)
    #   print(status)
    time.sleep(0.2)
finally:
  GPIO.cleanup()
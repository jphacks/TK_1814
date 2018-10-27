
from time import sleep
import RPi.GPIO as GPIO
MICPIN = 4
LEDPIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(MICPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LEDPIN, GPIO.OUT)

status = 'WAIT'

def record():
  global status

  status = 'RECORD'
  print("hoge")
  sleep(1)
  
  status = 'WAIT'

def micCallback(channnel):
  record()

def checkLED(): 
  if status == 'WAIT':
     GPIO.output(LEDPIN, GPIO.HIGH)
  elif status == 'RECORD':
     GPIO.output(LEDPIN, GPIO.LOW)

GPIO.add_event_detect(MICPIN, GPIO.RISING, callback=micCallback, bouncetime=300)

try:
  while True:
    checkLED()
    sleep(0.01)

except KeyboardInterrupt:
  pass

GPIO.cleanup()

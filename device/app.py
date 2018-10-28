import pyaudio
import wave
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import datetime
import requests
import json
import threading

MICPIN = 27
SPICS = 8
SPIMISO = 9
SPIMOSI = 10
SPICLK = 11
LEDPIN = 17
USER_ID = 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(MICPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(LEDPIN, GPIO.OUT)
GPIO.setup(LEDPIN, GPIO.OUT)

status = 'WAIT'
numOfTouch = 0
touchLogList = []
axisVal = [0.0, 0.0, 0.0]
axisPrevVal = [0.0, 0.0, 0.0]
promiseID = 0

def initialize():
  global status
  global promiseID

  status = 'WAIT'
  promiseID = 0


def record():
  global status
  global promiseID

  status = 'RECORD'

  CHUNK = 1024
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 48000
  RECORD_SECONDS = 5
  WAVE_OUTPUT_FILENAME = "output.wav"

  p = pyaudio.PyAudio()

  stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

  print("* recording")

  frames = []

  for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read(CHUNK, exception_on_overflow = False)
      buf = np.frombuffer(data, dtype="int16") # 読み込んだストリームデータを2byteのInt型のリストに分離
      frames.append(b''.join(buf[::3])) # 記録するデータを1/3に間引いてリストを結合してフレームに追加


  print("* done recording")

  stream.stop_stream()
  stream.close()
  p.terminate()

  wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE / 3) # ヘッダのサンプリングレートを16kHzにする
  wf.writeframes(b''.join(frames))
  wf.close()

  status = 'WAITING_RESPONSE'

  URL = 'https://pinky.kentaiwami.jp/record'
  files = {'wav': open(WAVE_OUTPUT_FILENAME, 'rb')}
  data = {'id': '9'}
  r = requests.post(URL, files=files, data=data)
  print(r)
  print(r.json())

  promiseID = r.json()['promise']['id']

  status = 'PROMISE'

def readadc(adcnum):
    global SPICS
    global SPIMISO
    global SPIMOSI
    global SPICLK

    if adcnum > 7 or adcnum < 0:
        return -1

    GPIO.output(SPICS, GPIO.HIGH)
    GPIO.output(SPICLK, GPIO.LOW)
    GPIO.output(SPICS, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3    # LSBから8ビット目を送信するようにする

    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(SPIMOSI, GPIO.HIGH)
        else:
            GPIO.output(SPIMOSI, GPIO.LOW)
        commandout <<= 1
        GPIO.output(SPICLK, GPIO.HIGH)
        GPIO.output(SPICLK, GPIO.LOW)
    adcout = 0
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(SPICLK, GPIO.HIGH)
        GPIO.output(SPICLK, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(SPIMISO)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(SPICS, GPIO.HIGH)
    return adcout

def checkTouch():
  global axisVal
  global numOfTouch
  global touchLogList
  global status
  global USER_ID
  global promiseID

  axisVal[0] = readadc(0)
  axisVal[1] = readadc(1)
  axisVal[2] = readadc(2)

  if axisPrevVal[0] != 0.0:
    if axisVal[0] - axisPrevVal[0] > 700 or axisVal[1] - axisPrevVal[1] > 700 or axisVal[2] - axisPrevVal[2] > 700:
      now = datetime.datetime.now()
      nowStr = now.strftime("%Y-%m-%d %H:%M:%S")
      print("yay its touching!!")
      sleep(0.5)

      print(nowStr)

      url = 'https://pinky.kentaiwami.jp/motion'
      s = requests.session()
      headers = {"Content-Type" : "application/json"}
      params = {'promise_id':promiseID, 'created_at':nowStr, 'user_id':USER_ID}
      r = s.post(url, data=json.dumps(params),headers=headers)
      print(r.text.encode('utf-8'))
      sleep(0.5)

  axisPrevVal[0] = axisVal[0]
  axisPrevVal[1] = axisVal[1]
  axisPrevVal[2] = axisVal[2]
  print(axisVal)
  print(axisPrevVal)
  sleep(0.2)


def micCallback(channnel):
  if status == 'WAIT':
    t=threading.Timer(20,initialize)
    t.start()
    record()


def checkLED():
  if status == 'WAIT':
     GPIO.output(LEDPIN, GPIO.LOW)
  elif status == 'RECORD':
     GPIO.output(LEDPIN, GPIO.HIGH)
  elif status == 'WAITING_RESPONSE':
     GPIO.output(LEDPIN, GPIO.LOW)
  elif status == 'PROMISE':
     GPIO.output(LEDPIN, GPIO.HIGH)

GPIO.add_event_detect(MICPIN, GPIO.RISING, callback=micCallback, bouncetime=300)

try:
  while True:
    checkLED()
    if status == 'PROMISE' and promiseID != 0:
      checkTouch()
    sleep(0.01)

except KeyboardInterrupt:
  pass

GPIO.cleanup()

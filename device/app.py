
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

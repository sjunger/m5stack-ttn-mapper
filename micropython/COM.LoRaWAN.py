# M5Stack (Core) TTN-Mapper device
#
# Version: 2.2 (2021-05-08)
# License: GNU General Public License v3.0
# Author: Stefan Junger

from m5stack import *
from m5ui import *
from uiflow import *
import time

setScreenColor(0x222222)


x = None
string = None
battery = None
batterycharge = None


label0 = M5TextBox(0, 90, "device status", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
label1 = M5TextBox(32, 18, "battery", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label2 = M5TextBox(0, 58, "last event:", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
line0 = M5Line(M5Line.PLINE, 0, 44, 320, 44, 0xFFFFFF)
line1 = M5Line(M5Line.PLINE, 0, 200, 320, 200, 0xFFFFFF)
circle0 = M5Circle(302, 22, 8, 0xff0303, 0xff0000)
label3 = M5TextBox(10, 212, "status", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
circle1 = M5Circle(18, 22, 8, 0x333333, 0xff0000)
label4 = M5TextBox(280, 218, "V2.2", lcd.FONT_Default, 0xFFFFFF, rotate=0)


# Beschreibe diese Funktion...
def AT(x):
  global string, battery, batterycharge
  uart1.write(str((str('AT+') + str(x))))
  wait_ms(100)
  string = (uart1.read()).decode()
  label0.setText(str(string))
  wait_ms(500)

# Beschreibe diese Funktion...
def LED_green_blink():
  global x, string, battery, batterycharge
  rgb.setBrightness(4)
  for count in range(1):
    rgb.setColorFrom(6 , 10 ,0x33ff33)
    rgb.setColorFrom(1 , 5 ,0x33ff33)
    wait_ms(2000)
    rgb.setColorFrom(6 , 10 ,0x000000)
    rgb.setColorFrom(1 , 5 ,0x000000)
    wait_ms(2000)

# Beschreibe diese Funktion...
def LED_red_blink():
  global x, string, battery, batterycharge
  rgb.setBrightness(4)
  for count2 in range(1):
    rgb.setColorFrom(6 , 10 ,0xff0000)
    rgb.setColorFrom(1 , 5 ,0xff0000)
    wait_ms(100)
    rgb.setColorFrom(6 , 10 ,0x000000)
    rgb.setColorFrom(1 , 5 ,0x000000)
    wait_ms(2900)


def buttonB_wasPressed():
  global x, string, battery, batterycharge
  label3.setText('sending message ...')
  circle0.setBgColor(0x3366ff)
  circle0.setBorderColor(0x3366ff)
  rgb.setColorFrom(6 , 10 ,0x3333ff)
  rgb.setColorFrom(1 , 5 ,0x3333ff)
  AT('SendHex=CAFE')
  wait_ms(2000)
  circle0.setBgColor(0xffff00)
  circle0.setBorderColor(0xffff33)
  rgb.setColorFrom(6 , 10 ,0xffff00)
  rgb.setColorFrom(1 , 5 ,0xffff00)
  label3.setText('wait ...')
  wait_ms(3000)
  label3.setText('ready-to-transmit ...')
  circle0.setBgColor(0x33cc00)
  circle0.setBorderColor(0x33cc00)
  rgb.setColorFrom(6 , 10 ,0x000000)
  rgb.setColorFrom(1 , 5 ,0x000000)
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonC_wasPressed():
  global x, string, battery, batterycharge
  AT('DevAddr=?')
  label3.setText('ready-to-transmit ...')
  rgb.setColorFrom(6 , 10 ,0x000000)
  rgb.setColorFrom(1 , 5 ,0x000000)
  circle0.setBgColor(0x33cc00)
  circle0.setBorderColor(0x33cc00)
  pass
btnC.wasPressed(buttonC_wasPressed)


uart1 = machine.UART(1, tx=17, rx=16)
uart1.init(115200, bits=8, parity=None, stop=1)
circle0.setBgColor(0xff0000)
circle0.setBorderColor(0xff0000)
circle1.setBorderColor(0xff0000)
circle1.setBgColor(0x333333)
rgb.setColorFrom(6 , 10 ,0xffff00)
rgb.setColorFrom(1 , 5 ,0xffff00)
label0.setText('')
label3.setText('initialization ...')
AT('LORAWAN=1')
AT('OTAA=0')
AT('IsTxConfirmed=0')
AT('ADR=0')
AT('AppPort=10')
AT('DevAddr=<DevAddr>')
AT('NwkSKey=<NwkSKey>')
AT('AppSKey=<AppSKey>')
AT('Join=1')
circle0.setBgColor(0x33cc00)
circle0.setBorderColor(0x33cc00)
rgb.setColorFrom(6 , 10 ,0x000000)
rgb.setColorFrom(1 , 5 ,0x000000)
label3.setText('ready-to-transmit ...')
while True:
  label1.setText(str((str((power.getBatteryLevel())) + str('%'))))
  battery = power.getBatteryLevel()
  batterycharge = power.isCharging()
  if batterycharge == 1:
    circle1.setBorderColor(0x33ff33)
    circle1.setBgColor(0x000000)
    LED_green_blink()
  else:
    if battery > 50:
      circle1.setBorderColor(0x33ff33)
      circle1.setBgColor(0x33ff33)
    else:
      if battery > 25:
        circle1.setBorderColor(0xffff00)
        circle1.setBgColor(0xffff00)
      else:
        circle1.setBorderColor(0xcc0000)
        circle1.setBgColor(0xcc0000)
        LED_red_blink()
  wait_ms(2)

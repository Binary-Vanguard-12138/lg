#!/usr/bin/env python
"""
lg_mcp4131.py
2021-01-09
Public Domain

http://abyz.me.uk/lg/py_lgpio.html
http://abyz.me.uk/lg/py_rgpio.html
"""

class MCP4131:
   """
   DIG POT

   CS      1 o o 8 V+
   SCLK    2 o o 7 B
   SDI/SDO 3 o o 6 W
   GND     4 o o 5 A

   For this module nothing is read from the chip so the SBC's
   MISO line need not be connected.

   For safety put a resistor in series between MOSI and SDI/SDO.
   """
   def __init__(self, sbc, channel, device, speed=1e6, flags=0,
      wiper_value=64, chip_select=None, chip_deselect=None):
      """
      """
      self._sbc = sbc
      self._chip_select = chip_select
      self._chip_deselect = chip_deselect
      self._dac = sbc.spi_open(channel, device, speed, flags)
      self._wiper_value = wiper_value
      self.set_wiper(wiper_value)

   def set_wiper(self, value):
      assert 0 <= value <= 128
      self._wiper_value = value

      if self._chip_select is not None:
         self._chipselect

      self._sbc.spi_write(self._dac, [0, value])

      if self._chip_deselect is not None:
         self._chipdeselect

   def get_wiper(self):
      return self._wiper_value

   def increment_wiper(self):
      if self._wiper_value < 128:
         self.set_wiper(self._wiper_value + 1)

   def decrement_wiper(self):
      if self._wiper_value > 0:
         self.set_wiper(self._wiper_value - 1)

   def close(self):
      self._sbc.spi_close(self._dac)

if __name__ == "__main__":

   RGPIO = False # set to True if using rgpio, False if using lgpio

   import time
   import lg_mcp4131

   if RGPIO:

      import rgpio
      sbc = rgpio.sbc()
      if not sbc.connected:
         exit()

   else:

      import lgpio as sbc

   dac = lg_mcp4131.MCP4131(sbc, 0, 0, 50000)

   for i in range(129):
      dac.set_wiper(i)
      time.sleep(0.2)

   dac.close()

   if RGPIO:
      sbc.stop()


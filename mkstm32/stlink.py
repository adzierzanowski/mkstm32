import re
import sys
import subprocess

import serial
from serial.tools.list_ports import comports

from mkstm32.helpers import Option

# This class is responsible for ST-Link connection and operations
class STLink:
  def __init__(self, cli):
    self.cli = cli

  # Returns a list of connected devices
  @staticmethod
  def devices():
    p = subprocess.Popen(['st-info', '--probe'], stdout=subprocess.PIPE)
    data, _ = p.communicate()
    data = data.decode('utf8')

    # Get names of the devices
    name_regex = re.compile(r'descr: (.+)')
    names = name_regex.findall(data)

    # Get serial numbers
    serial_regex = re.compile(r'serial: (.+)')
    serials = serial_regex.findall(data)

    # Zip them together
    devices_ = list(zip(names, serials))

    return devices_

  # Prints detailed information about connected devices
  def probe(self):
    self.cli.call(['st-info', '--probe'])

  # Resets the MCU
  def reset(self):
    serial_ = self.cli.choose_serial()
    if serial_ is None:
      self.cli.call(['st-flash', 'reset'])
    else:
      self.cli.call(['st-flash', '--serial', serial_, 'reset'])

  # Starts a serial monitor on a specific port
  def monitor(self, port):
    if port is None:
      ports = [Option('{0:40} {1:20}'.format(p.device, p.description), p) for p in comports()]
      port = self.cli.choose(ports).device
      print(port)

    s = None
    try:
      s = serial.Serial(port=port)
    except serial.serialutil.SerialException:
      self.cli.print('Serial port failure: {}'.format(port), error=True)

    if s is None:
      sys.exit(1)

    try:
      while True:
        try:
          sys.stdout.write(s.read().decode('utf8'))
        except UnicodeDecodeError:
          pass

    except KeyboardInterrupt:
      sys.exit()

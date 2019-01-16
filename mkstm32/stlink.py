import re
import sys
import subprocess

import serial
from serial.tools.list_ports import comports

from mkstm32.cli import Option

class STLink:
  def __init__(self, cli):
    self.cli = cli

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

  def probe(self):
    self.cli.call(['st-info', '--probe'])

  def reset(self):
    devices = [Option('{0:20} {1:40}'.format(device[0],
              device[1]), device) for device in STLink.devices()]

    if not devices:
      self.cli.print('Could not find any ST-Link devices.', error=True)
      sys.exit(1)

    if len(devices) > 1:
      serial_ = self.cli.choose(devices)[1]
      self.cli.call(['st-flash', '--serial', serial_, 'reset'])
    else:
      self.cli.call(['st-flash', 'reset'])

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

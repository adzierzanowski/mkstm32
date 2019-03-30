import re
import sys
import time
import subprocess
import threading

import serial
from serial.tools.list_ports import comports

from mkstm32.helpers import Option

class STLink:
  '''This class is responsible for ST-Link connection and operations.'''

  def __init__(self, cli):
    self.cli = cli

  @staticmethod
  def devices():
    '''Returns a list of connected devices.'''

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

  def list_ports(self):
    '''Lists available serial ports'''
    for i, p in enumerate(comports()):
      print('{0:10} {1}'.format(self.cli.bold(i), p))

  def monitor(self, port, baud_rate=9600):
    '''Starts a serial monitor on a specific port.'''

    def thread_wrapper(func):
      def wrapper(*args, **kwargs):
        try:
          func(*args, **kwargs)

        except UnicodeDecodeError:
          pass

        except UnicodeEncodeError:
          pass

        except serial.serialutil.SerialException:
          self.cli.print('SerialException occurred.', warning=True)
          self.cli.print('Resetting connection...')
          time.sleep(1)
          self.monitor(port, baud_rate)

        except KeyboardInterrupt:
          sys.exit()

      return wrapper

    @thread_wrapper
    def keyboard_input(serial_interface):
      while True:
        text = input()
        serial_interface.write(text.encode() + b'\n')

    @thread_wrapper
    def serial_output(serial_interface):
      while True:
        sys.stdout.write(serial_interface.read().decode())

    if port is None:
      ports = [Option('{0:40} {1:20}'.format(p.device, p.description), p) for p in comports()]
      port = self.cli.choose(ports).device
      print('Listening on port: {}\n'.format(port))

    s = None
    try:
      s = serial.Serial(port=port, baudrate=baud_rate)
    except serial.serialutil.SerialException:
      self.cli.print('Serial port failure: {}'.format(port), error=True)

    if s is None:
      sys.exit(1)

    keyboard_input_thread = threading.Thread(
      target=keyboard_input,
      args=[s],
      daemon=True
    )

    serial_output_thread = threading.Thread(
      target=serial_output,
      args=[s],
      daemon=True
    )

    keyboard_input_thread.start()
    serial_output_thread.start()

    while True:
      try:
        pass
      except KeyboardInterrupt:
        sys.exit()

  def probe(self):
    '''Prints detailed information about connected devices.'''

    self.cli.call(['st-info', '--probe'])

  def reset(self):
    '''Resets the MCU.'''

    serial_ = self.cli.choose_serial()
    if serial_ is None:
      self.cli.call(['st-flash', 'reset'])
    else:
      self.cli.call(['st-flash', '--serial', serial_, 'reset'])
